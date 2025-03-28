import asyncio
import threading
import time
import atexit
import logging
from typing import Callable, List, Iterable, Generic, Awaitable, TypeVar, Union, Optional
from concurrent.futures import Future

from pybatcher.exceptions import BatchNotReadyError

from .batch import Batch

from .utils import Lock

T_in = TypeVar("T_in")
T_out = TypeVar("T_out")

logger = logging.getLogger(__name__)

class Batcher(Generic[T_in, T_out]):
    def __init__(self,
                 process_function: Callable[[List[T_in]], Union[Iterable[T_out], Awaitable[Iterable[T_out]]]], 
                 batch_delay: Optional[float] = None,
                 min_batch_size: int = 1, 
                 max_batch_size: Optional[int] = None, 
                 strict_batch_size: bool = False,
                 loop: Optional[asyncio.AbstractEventLoop] = None):
        """Crée un gestionnaire de traitement par lots (batcher).
        
        Le batcher permet de regrouper plusieurs requêtes individuelles pour les traiter
        ensemble en un seul appel à la fonction de traitement, ce qui peut améliorer
        les performances lorsqu'il est plus efficace de traiter des requêtes en groupe.
        
        :param process_function: Fonction (synchrone ou asynchrone) qui traite la liste des données du batch.
        :type process_function: Callable[[List[T_in]], Union[Iterable[T_out], Awaitable[Iterable[T_out]]]]
        :param batch_delay: Délai en secondes avant traitement automatique du batch. Si None, le batch est traité manuellement ou lorsqu'il est plein.
        :type batch_delay: Optional[float]
        :param min_batch_size: Taille minimale du batch avant traitement. Par défaut 1.
        :type min_batch_size: Optional[int]
        :param max_batch_size: Taille maximale du batch. Si atteint, le batch est traité immédiatement.
        :type max_batch_size: Optional[int]
        :param strict_batch_size: Si True, attend que le batch atteigne la taille exacte min_batch_size avant traitement.
        :type strict_batch_size: Optional[bool]
        :param loop: Boucle d'événements asyncio. Si non spécifiée, une nouvelle boucle est créée dans un thread distinct.
        :type loop: Optional[asyncio.AbstractEventLoop]
        
        :raises ValueError: Si batch_delay est négatif ou nul, si min_batch_size est négatif ou nul, 
                           ou si max_batch_size est inférieur ou égal à min_batch_size.
        """
        if batch_delay is not None and batch_delay <= 0:
            raise ValueError("batch_delay must be greater than 0.")
        if min_batch_size <= 0:
            raise ValueError("min_batch_size must be greater than 0.")
        if max_batch_size is not None and max_batch_size <= min_batch_size:
            raise ValueError("max_batch_size must be greater than min_batch_size.")
        
        self.batch_delay = batch_delay
        self.process_function = process_function
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        self.strict_batch_size = strict_batch_size
        self.current_batch = None
        self.lock = Lock()
        self.thread = None
        self.loop = loop

        logger.info(f"Initialized Batcher with min_batch_size={min_batch_size}, "
                   f"max_batch_size={max_batch_size}, batch_delay={batch_delay}, "
                   f"strict_batch_size={strict_batch_size}")

        if loop is None:
            logger.debug("No event loop provided, creating a new one in a separate thread")
            atexit.register(self.close)
            started_event = threading.Event()
            self.thread = threading.Thread(target=self._start_new_loop, args=(started_event,))
            self.thread.daemon = True
            self.thread.start()
            started_event.wait()

    def _start_new_loop(self, started_event: threading.Event):
        """Démarre une nouvelle boucle d'événements asyncio dans le thread actuel.
        
        Cette méthode est utilisée en interne lorsque aucune boucle d'événements n'est fournie
        au constructeur. La boucle créée s'exécutera jusqu'à ce que la méthode close() soit appelée.
        """
        logger.debug("Starting new event loop in separate thread")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        started_event.set()
        logger.debug("Event loop started and running")
        self.loop.run_forever()
        logger.debug("Event loop stopped")
        

    def create_batch(self):
        """Crée un nouveau batch pour traiter les requêtes.
        
        :return: Un nouvel objet Batch configuré avec les paramètres du batcher.
        :rtype: Batch
        """
        logger.debug("Creating new batch")
        return Batch(process_function=self.process_function, 
                     loop=self.loop, 
                     min_size=self.min_batch_size,
                     max_size=self.max_batch_size, 
                     strict_size=self.strict_batch_size,
                     auto_start_delay=self.batch_delay, 
                     auto_start_when_full=True)

    def submit_request(self, request_data: T_in) -> Future[T_out]:
        """Soumet une requête en l'ajoutant à un batch.
        
        Crée un nouveau batch si nécessaire, ou ajoute la requête au batch en cours
        s'il peut encore accepter des requêtes.
        
        :param request_data: Donnée de la requête à traiter.
        :type request_data: T_in
        
        :return: Un objet Future qui sera résolu avec le résultat correspondant à cette requête.
        :rtype: concurrent.futures.Future
        """
        with self.lock:
            if self.current_batch is None or not self.current_batch.can_add_request():
                logger.debug("Creating new batch for request as current batch is None or full")
                self.current_batch = self.create_batch()
            
            logger.debug("Submitting request to batch")
            return self.current_batch.add_request(request_data)

    def flush(self):
        """Lance le traitement du batch en cours s'il est prêt.
        
        Si le batch en cours contient suffisamment de requêtes selon les paramètres configurés,
        cette méthode déclenche son traitement immédiat. Le batch en cours est ensuite réinitialisé.
        
        :raises BatchNotReadyError: Si le batch n'est pas prêt.
        """
        with self.lock:
            if self.current_batch is not None:
                try:
                    logger.info("Flushing current batch")
                    self.current_batch.start()
                    logger.info("Batch flushed successfully")
                except BatchNotReadyError:
                    logger.warning("Cannot flush batch: batch not ready")
                    raise
                self.current_batch = None
            else:
                logger.debug("No batch to flush")
    
    async def handle_request(self, request_data: T_in) -> T_out:
        """Gère une requête de manière asynchrone en l'ajoutant à un batch.
        
        Cette méthode est l'équivalent asynchrone de submit_request, permettant
        d'attendre directement le résultat de la requête avec 'await'.
        
        :param request_data: Donnée de la requête à traiter.
        :type request_data: T_in
        
        :return: Le résultat individuel correspondant à cette requête.
        :rtype: T_out
        """
        logger.debug("Handling asynchronous request")
        return await asyncio.wrap_future(self.submit_request(request_data))

    def close(self, timeout: Optional[float] = None):
        """Ferme le batcher en traitant le batch en cours si celui-ci est prêt et en arrêtant la boucle d'événements.
        
        Cette méthode doit être appelée pour libérer les ressources lorsque le batcher n'est plus nécessaire.
        Si le batcher a créé sa propre boucle d'événements, celle-ci est arrêtée.
        
        :param timeout: Temps maximum en secondes pour attendre la fin du traitement. 
                       Si None, attend indéfiniment.
        :type timeout: Optional[float]
        """
        logger.info(f"Closing batcher with timeout={timeout}")
        start_time = time.time()
        if self.lock.acquire(timeout=timeout):
            try:
                if self.current_batch is not None:
                    try:
                        timeout_remaining = max(0, timeout - (time.time() - start_time)) if timeout is not None else None
                        logger.debug(f"Starting final batch with timeout={timeout_remaining}")
                        self.current_batch.start(blocking=True, timeout=timeout_remaining)
                    except BatchNotReadyError:
                        logger.warning("Final batch not ready for processing during close")
                    else:
                        try:
                            timeout_remaining = max(0, timeout - (time.time() - start_time)) if timeout is not None else None
                            logger.debug(f"Waiting for final batch results with timeout={timeout_remaining}")
                            self.current_batch.results(timeout=timeout_remaining)
                            logger.debug("Final batch processing completed")
                        except Exception as e:
                            logger.error(f"Error processing final batch during close: {str(e)}", exc_info=True)
                            # Le batcher ne gère pas les erreurs de traitements, elles seront propagées via les futures
                if self.thread is not None and not self.loop.is_closed():
                    logger.debug("Stopping event loop")
                    self.loop.call_soon_threadsafe(self.loop.stop)
                    timeout_remaining = max(0, timeout - (time.time() - start_time)) if timeout is not None else None
                    logger.debug(f"Joining thread with timeout={timeout_remaining}")
                    self.thread.join(timeout=timeout_remaining)
                    self.loop.close()
                    logger.info("Event loop closed")
            finally:
                self.lock.release()
        else:
            logger.error(f"Timeout error while waiting for lock during close (timeout={timeout}s)")
            raise TimeoutError("Timeout while waiting for lock release.")
        logger.info("Batcher closed successfully")
