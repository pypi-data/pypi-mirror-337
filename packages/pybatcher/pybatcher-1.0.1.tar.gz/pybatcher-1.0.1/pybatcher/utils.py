import threading
import asyncio
import collections
from concurrent.futures import Future


class WrappedFuture(asyncio.Future):
    def __init__(self, future: Future, loop=None):
        loop = loop or asyncio.get_event_loop()
        from datetime import datetime
        def _done_callback(fut):
            print(f"{datetime.now()} done_callback_from_wf fut={fut}")
            def debug_wrap(f):
                def wrapper(*args, **kwargs):
                    print(f"debug_wrap f={f}")
                    return f(*args, **kwargs)

            if fut.cancelled():
                loop.call_soon_threadsafe(debug_wrap(self.cancel))
            elif fut.exception():
                loop.call_soon_threadsafe(debug_wrap(self.set_exception), fut.exception())
            else:
                loop.call_soon_threadsafe(debug_wrap(self.set_result),fut.result())
        future.add_done_callback(_done_callback)
        super().__init__(loop=loop)


class Lock:
    def __init__(self):
        self._locked = False
        self._waiters = collections.deque()  # Liste des waiters communs : ('sync', threading.Event) ou ('async', asyncio.Future)
        self._state_lock = threading.Lock()  # Pour protéger l'accès partagé

    def acquire(self, blocking=True, timeout=None):
        """Se comporte comme threading.Lock.acquire."""
        with self._state_lock:
            if not self._locked and not self._waiters:
                self._locked = True
                return True

            if not blocking:
                return False

            waiter = threading.Event()
            self._waiters.append(('sync', waiter))
        
        acquired = waiter.wait(timeout)
        if not acquired:
            with self._state_lock:
                # Retirer le waiter en cas de timeout.
                self._waiters.remove(('sync', waiter))
            return False
            
        return True

    async def async_acquire(self):
        """Se comporte comme asyncio.Lock.acquire et gère aussi l'annulation."""
        with self._state_lock:
            if not self._locked and not self._waiters:
                self._locked = True
                return True

            loop = asyncio.get_running_loop()
            fut = loop.create_future()
            self._waiters.append(('async', fut))
        
        try:
            await fut
        except Exception:
            with self._state_lock:
                # Si l'attente a été annulée ou échoue, retirer le waiter de la file.
                if ('async', fut) in self._waiters:
                    self._waiters.remove(('async', fut))
            raise
        return True

    def release(self):
        """Libère le verrou et réveille le premier waiter en file s'il existe."""
        with self._state_lock:
            if not self._locked:
                raise RuntimeError("Tentative de release d'un verrou non acquis.")

            # Recupère le premier waiter en file qui n'est pas déjà terminé (async).
            while self._waiters:
                waiter_type, waiter = self._waiters.popleft()
                if waiter_type == 'sync' or not waiter.done():
                    break
            else:
                waiter_type = None
                self._locked = False

        if waiter_type == 'sync':
            waiter.set()
        elif waiter_type == 'async':
            if not waiter.done():
                loop = waiter.get_loop()
                loop.call_soon_threadsafe(waiter.set_result, True)
            else:
                # Rare cas où le waiter a été annulé avant d'être réveillé.
                # On recommence la libération pour réveiller le prochain waiter.
                self.release()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    async def __aenter__(self):
        await self.async_acquire()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.release()


def start_task(task: asyncio.Task, done_event=None):
    """Démarre une tâche asyncio si elle n'est pas déjà démarrée."""
    async def awaiter():
        if not task.done():
            await task
        if done_event:
            done_event.set()
    task.get_loop().call_soon_threadsafe(awaiter)
