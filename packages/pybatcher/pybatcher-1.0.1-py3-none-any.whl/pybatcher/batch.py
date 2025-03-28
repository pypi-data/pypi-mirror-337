import asyncio
import threading
import logging
from typing import Callable, List, Iterable, TypeVar, Generic, Awaitable, Optional, Union
from concurrent.futures import CancelledError, Future, TimeoutError

from .exceptions import BatchNotReadyError, FullBatchError
from .utils import Lock, start_task

T_in = TypeVar("T_in")
T_out = TypeVar("T_out")

# Create a logger for this module
logger = logging.getLogger("pybatcher.batch")


class Batch(Generic[T_in]):
    """
    Gère un traitement par lots de données.
    
    Cette classe permet de regrouper des requêtes individuelles pour les traiter en lot,
    offrant ainsi une meilleure performance pour certains types de traitement.
    
    :param process_function: Fonction qui traite les données en lot
    :type process_function: Callable[[List[T_in]], Union[Iterable[T_out], Awaitable[Iterable[T_out]]]]
    :param loop: Boucle d'événements asyncio à utiliser, utilise la boucle courante si non spécifié
    :type loop: Optional[asyncio.AbstractEventLoop]
    :param max_size: Taille maximale du lot, None pour illimité
    :type max_size: Optional[int]
    :param min_size: Taille minimale du lot pour démarrer le traitement
    :type min_size: Optional[int]
    :param strict_size: Taille stricte du lot, True pour ne compter que les requêtes non annulées
    :type strict_size: bool
    :param auto_start_delay: Délai en secondes avant démarrage automatique du traitement
    :type auto_start_delay: Optional[float]
    :param auto_start_when_full: Démarre automatiquement le traitement quand le lot est plein
    :type auto_start_when_full: bool
    """
    def __init__(self, 
                 process_function: Callable[[List[T_in]], Union[Iterable[T_out],Awaitable[Iterable[T_out]]]], 
                 loop: Optional[asyncio.AbstractEventLoop] = None, 
                 max_size: Optional[int] = None, 
                 min_size: Optional[int] = 1,
                 strict_size: bool = False,
                 auto_start_delay: Optional[float] = None, 
                 auto_start_when_full: bool = False):
        if min_size is not None and min_size < 0:
            raise ValueError("min_size doit être supérieur ou égal à 0.")
        if max_size is not None and max_size < min_size:
            raise ValueError("max_size doit être supérieur ou égal à min_size.")
        if auto_start_delay is not None and auto_start_delay < 0:
            raise ValueError("auto_start_delay doit être positif ou None.")

        self.requests = []
        self.start_event = asyncio.Event()
        self.loop = loop or asyncio.get_event_loop()
        if self.loop is None or self.loop.is_closed():
            raise RuntimeError("Event loop not set or closed.")
        self.lock = Lock()
        self.min_size = min_size
        self.strict_size = strict_size
        self.max_size = max_size
        self.start_when_full = auto_start_when_full and max_size
        self.task = self.loop.create_task(self._process(process_function))
        start_task(self.task)
        self.timer = None
        self.auto_start_delay = auto_start_delay
        
        logger.info(f"Initialized Batch with min_size={min_size}, max_size={max_size}, "
                   f"strict_size={strict_size}, auto_start_delay={auto_start_delay}, "
                   f"auto_start_when_full={auto_start_when_full}")
        
    def __len__(self):
        if not self.strict_size:
            return len(self.requests)
        return len([f for _, f in self.requests if not f.cancelled()])
        
    def start(self, blocking: bool = True, timeout: Optional[float] = None):
        """
        Démarre le traitement du lot.
        Si blocking est True, attend que le traitement soit démarré. 
        Si non, retourne immédiatement après avoir programmé le démarrage.

        :param blocking: Attend que le traitement soit démarré
        :type blocking: bool
        :param timeout: Délai maximum d'attente en secondes, None pour attente illimitée
        :type timeout: Optional[float]
        :raises BatchNotReadyError: Si le lot n'est pas prêt à être traité
        """
        if timeout is not None and not blocking:
            raise ValueError("Timeout can only be used with blocking=True.")
        
        if not self.ready():
            logger.warning("Attempt to start batch that is not ready")
            raise BatchNotReadyError("Batch not ready.")
            
        if self.timer and not self.timer.done():
            logger.debug("Cancelling timer as batch is starting manually")
            self.timer.cancel()
            self.timer = None
            
        logger.info(f"Starting batch with {len(self)} requests (blocking={blocking}, timeout={timeout})")
        
        if blocking:
            event = threading.Event()
            def blocking_start():
                event.set()
                self.start_event.set()
            
            self.loop.call_soon_threadsafe(blocking_start)
            event.wait(timeout=timeout)
            logger.debug("Batch start event completed")
        else:
            self.loop.call_soon_threadsafe(self.start_event.set)

    def set_timer(self, delay: float):
        """
        Démarre un timer pour démarrer le traitement automatiquement après un délai.
        
        :param delay: Délai en secondes avant démarrage
        :type delay: float
        :raises RuntimeError: Si le lot a déjà démarré ou est terminé
        """
        if self.started() or self.done():
            logger.warning("Cannot set timer: batch already started or completed")
            raise RuntimeError("Batch already started.")
        
        if self.timer and not self.timer.done():
            logger.debug("Cancelling existing timer")
            self.timer.cancel()
            self.timer = None
        
        logger.info(f"Setting auto-start timer with delay: {delay}")
        self.timer = self.loop.create_task(self._timer(delay))
        start_task(self.timer)

    async def _timer(self, delay: float):
        """
        Méthode interne qui gère le démarrage automatique après un délai.
        
        :param delay: Délai en secondes avant démarrage
        :type delay: float
        :raises RuntimeError: Si le lot n'est pas prêt après le délai
        """
        logger.debug(f"Timer started, batch will auto-start in {delay} seconds")
        await asyncio.sleep(delay)
        if not self.ready():
            logger.warning("Timer expired but batch not ready")
            self.timer = None
            raise BatchNotReadyError("Batch not ready.")
        logger.info(f"Timer expired, auto-starting batch with {len(self)} requests")
        self.start_event.set()

    async def _process(self, process_function: Callable[[List[T_in]], Union[Iterable[T_out],Awaitable[Iterable[T_out]]]]):
        """
        Méthode interne qui traite les données du lot.
        
        :param process_function: Fonction qui traite les données en lot
        :type process_function: Callable[[List[T_in]], Union[Iterable[T_out], Awaitable[Iterable[T_out]]]]
        """
        await self.start_event.wait()
        logger.debug("Start event received, beginning batch processing")
        
        data_list = []
        futures = []

        async with self.lock:
            for req_data, future in self.requests:
                if future.set_running_or_notify_cancel():
                    data_list.append(req_data)
                    futures.append(future)
        
        request_count = len(data_list)
        logger.info(f"Processing batch with {request_count} active requests")
        
        if request_count > 0:
            try:
                if asyncio.iscoroutinefunction(process_function):
                    logger.debug("Executing async process function")
                    results = await process_function(data_list)
                else:
                    logger.debug("Executing sync process function")
                    results = process_function(data_list)
                    
                logger.debug(f"Process function returned {len(results) if hasattr(results, '__len__') else 'unknown'} results")
            except Exception as e:
                logger.error(f"Error during batch processing: {str(e)}", exc_info=True)
                for future in futures:
                    future.set_exception(e)
                raise # Propagate exception
            else: 
                result_count = 0
                for future, result in zip(futures, results):
                    if not future.done():
                        future.set_result(result)
                        result_count += 1
                logger.info(f"Batch processing completed, set {result_count} results")
    
    def ready(self) -> bool:
        """
        Vérifie si le lot est prêt à être traité.
        
        Un lot est prêt s'il contient au moins min_size requêtes, n'a pas encore démarré
        et n'est pas terminé.
        
        :return: True si le lot est prêt à être traité, False sinon
        :rtype: bool
        """
        is_ready = not self.start_event.is_set() and not self.task.done() and len(self) >= self.min_size
        logger.debug(f"Batch ready check: {is_ready} (size={len(self)}, min_size={self.min_size})")
        return is_ready
    
    def started(self) -> bool:
        """
        Vérifie si le traitement du lot a démarré.
        
        :return: True si le traitement a démarré, False sinon
        :rtype: bool
        """
        return self.start_event.is_set()

    def running(self) -> bool:
        """
        Vérifie si le lot est en cours d'exécution.
        
        :return: True si le lot est démarré mais pas encore terminé, False sinon
        :rtype: bool
        """
        return self.start_event.is_set() and not self.task.done()
    
    def done(self) -> bool:
        """
        Vérifie si le traitement du lot est terminé.
        
        :return: True si le traitement est terminé, False sinon
        :rtype: bool
        """
        return self.task.done()
    
    def cancel(self) -> bool:
        """
        Annule le lot si possible.
        
        :return: True si le lot a été annulé, False sinon (déjà démarré ou terminé)
        :rtype: bool
        """
        if self.start_event.is_set() or self.task.done():
            logger.debug("Cannot cancel: batch already started or completed")
            return False
        
        with self.lock:
            if self.timer:
                logger.debug("Cancelling batch timer")
                self.timer.cancel()
            if self.task.cancel():
                request_count = len(self.requests)
                logger.warning(f"Batch cancelled with {request_count} requests")
                for _, future in self.requests:
                    future.cancel()
                    future.set_running_or_notify_cancel() # notifie les waiters
                return True
        return False
    
    def cancelled(self) -> bool:
        """
        Vérifie si le lot a été annulé.
        
        :return: True si le lot a été annulé, False sinon
        :rtype: bool
        """
        return self.task.cancelled() or self.task.cancelling() > 0
    
    def is_full(self):
        """
        Vérifie si le lot a atteint sa capacité maximale.
        
        :return: True si le lot est plein, False sinon
        :rtype: bool
        """
        is_full = self.max_size is not None and len(self) >= self.max_size
        if is_full:
            logger.debug(f"Batch is full (size={len(self)}, max_size={self.max_size})")
        return is_full
    
    def is_empty(self):
        """
        Vérifie si le lot est vide.
        
        :return: True si le lot ne contient aucune requête, False sinon
        :rtype: bool
        """
        return len(self) == 0

    def can_add_request(self) -> bool:
        """
        Vérifie si une requête peut être ajoutée au lot.
        
        Une requête peut être ajoutée si le lot n'est pas plein, n'a pas démarré,
        et n'est pas terminé.
        
        :return: True si une requête peut être ajoutée, False sinon
        :rtype: bool
        """
        can_add = not self.done() and not self.started() and not self.is_full()
        logger.debug(f"Can add request check: {can_add}")
        return can_add

    def add_request(self, request_data) -> Future[T_out]:
        """
        Ajoute une requête au lot.
        
        :param request_data: Données de la requête à traiter
        :type request_data: T_in
        :return: Future qui sera résolue avec le résultat du traitement
        :rtype: Future[T_out]
        :raises RuntimeError: Si le lot a déjà démarré ou est terminé
        :raises FullBatchError: Si le lot est plein
        """
        with self.lock:
            if self.done() or self.started():
                logger.warning("Cannot add request: batch already started or completed")
                raise RuntimeError("Batch already started.")
            if self.is_full():
                logger.warning("Cannot add request: batch is full")
                raise FullBatchError("Batch is full.")
            
            future = Future()
            
            self.requests.append((request_data, future))
            current_size = len(self)
            logger.debug(f"Request added to batch, current size: {current_size}")

            if self.auto_start_delay and self.timer is None and current_size >= self.min_size:
                logger.debug(f"Starting auto-start timer with delay: {self.auto_start_delay}")
                self.set_timer(self.auto_start_delay)                
        if self.start_when_full and self.is_full():
            logger.info("Batch is full, triggering automatic start")
            self.start(blocking=False)
        return future

    def results(self, timeout: Optional[float] = None, include_cancelled: bool = True) -> List[Union[T_out, None]]:
        """
        Récupère les résultats du traitement du lot.
        
        :param timeout: Délai maximum d'attente en secondes, None pour attente illimitée
        :type timeout: Optional[float]
        :param include_cancelled: Inclure les résultats des requêtes annulées (None)
        :type include_cancelled: bool
        :return: Liste des résultats pour chaque requête (None pour les requêtes annulées)
        :rtype: List[T_out]
        :raises CancelledError: Si le lot a été annulé
        :raises TimeoutError: Si le délai d'attente est dépassé
        """
        if self.cancelled():
            logger.error("Cannot get results: batch was cancelled")
            raise CancelledError("Batch was cancelled.")
        
        logger.debug(f"Waiting for batch results (timeout={timeout}, include_cancelled={include_cancelled})")
        done_event = threading.Event()

        def done_callback(future):
            logger.debug("Batch processing completed callback triggered")
            done_event.set()

        if not self.task.done():    
            self.task.add_done_callback(done_callback)
            wait_result = done_event.wait(timeout=timeout)
            
            if not wait_result:
                logger.warning(f"Timeout exceeded waiting for batch results: {timeout}s")
                raise TimeoutError("Timeout exceeded.")

        # May raise exception if batch processing failed
        try:
            self.task.result()
            logger.debug("Successfully retrieved batch task result")
        except Exception as e:
            logger.error(f"Error retrieving batch results: {str(e)}")
            raise
        
        if include_cancelled:
            results = [(future.result() if not future.cancelled() else None) for _, future in self.requests]
        else:
            results = [future.result() for _, future in self.requests if not future.cancelled()]
            
        logger.info(f"Retrieved {len(results)} results from batch")
        return results
        
    def __del__(self):
        """
        Destructeur qui annule les tâches asynchrones si elles sont encore actives.
        """
        if hasattr(self, 'task') and not self.task.done():
            try:
                if not self.loop.is_closed():
                    logger.debug("Cancelling batch task in destructor")
                    self.task.cancel()
            except Exception:
                pass
        
        if hasattr(self, 'timer') and self.timer and not self.timer.done():
            try:
                if not self.loop.is_closed():
                    logger.debug("Cancelling batch timer in destructor")
                    self.timer.cancel()
            except Exception:
                pass

