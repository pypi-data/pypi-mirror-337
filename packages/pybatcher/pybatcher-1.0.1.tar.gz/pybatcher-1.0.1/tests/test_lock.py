import unittest
import threading
import asyncio
import time

from pybatcher.utils import Lock


class TestLockSync(unittest.TestCase):
    def test_release_without_acquire(self):
        lock = Lock()
        with self.assertRaises(RuntimeError):
            lock.release()

    def test_release_wakes_sync_waiter(self):
        lock = Lock()
        self.assertTrue(lock.acquire())
        
        waiter_event = threading.Event()

        def waiter():
            # This call should block until lock is released.
            lock.acquire()
            waiter_event.set()
            # Release the lock to not block further in case of other operations.
            lock.release()

        t = threading.Thread(target=waiter)
        t.start()
        # Give the thread some time to start and block
        time.sleep(0.1)
        # Release the lock to wake the waiting thread.
        lock.release()
        # Wait for the thread to set its event (with timeout)
        self.assertTrue(waiter_event.wait(timeout=1.0))
        t.join()

    def test_timeout(self):
        lock = Lock()
        self.assertTrue(lock.acquire())
        
        # Try to acquire the lock with timeout, should fail
        start_time = time.time()
        self.assertFalse(lock.acquire(timeout=0.2))
        elapsed = time.time() - start_time
        
        # Check that it waited approximately the timeout period
        self.assertGreaterEqual(elapsed, 0.2)
        self.assertLess(elapsed, 0.5)  # Provide some margin for slow systems
        
        # Release the original lock
        lock.release()

class TestLockAsync(unittest.IsolatedAsyncioTestCase):
    async def test_release_wakes_async_waiter(self):
        lock = Lock()
        acquired = await lock.async_acquire()
        self.assertTrue(acquired)
        
        waiter_event = asyncio.Event()

        async def waiter():
            # This call should block until lock is released.
            await lock.async_acquire()
            waiter_event.set()
            # Release the lock to avoid deadlock.
            lock.release()

        # Schedule the waiter coroutine as a task.
        task = asyncio.create_task(waiter())
        # Give the waiter a moment to start and get enqueued.
        await asyncio.sleep(0.1)
        # Release the lock to wake the async waiter.
        lock.release()
        # Wait until the waiter_event is set.
        await asyncio.wait_for(waiter_event.wait(), timeout=1.0)
        await task

    async def test_async_acquire_cancellation(self):
        lock = Lock()
        await lock.async_acquire()
        
        async def attempt_acquire():
            await lock.async_acquire()
            return True
        
        # Start task and cancel it immediately
        task = asyncio.create_task(attempt_acquire())
        await asyncio.sleep(0.1)  # Give task time to start and block
        
        task.cancel()
        
        with self.assertRaises(asyncio.CancelledError):
            await task
            
        # The lock should still be acquired
        self.assertFalse(lock.acquire(blocking=False))
        
        # Clean up
        lock.release()

    async def test_multiple_waiters_mixed_types(self):
        lock = Lock()
        await lock.async_acquire()
        
        # Keep track of wakeup order
        wakeup_order = []
        sync_event = threading.Event()
        timeout_event = threading.Event()
        
        # Create sync waiter
        def sync_waiter():
            lock.acquire()
            wakeup_order.append("sync")
            lock.release()
            sync_event.set()
        
        sync_thread = threading.Thread(target=sync_waiter)
        sync_thread.start()
        
        # Create sync waiter with timeout that will fail
        def sync_timeout_waiter():
            result = lock.acquire(timeout=0.2)  # This should timeout
            if result:
                wakeup_order.append("timeout_sync")
                lock.release()
            else:
                wakeup_order.append("timeout_sync_failed")
            timeout_event.set()
        
        timeout_thread = threading.Thread(target=sync_timeout_waiter)
        timeout_thread.start()
        
        # Create first async waiter
        async def async_waiter1():
            await lock.async_acquire()
            wakeup_order.append("async1")
            lock.release()
        
        # Create an async waiter that will be cancelled
        async def async_cancelled_waiter():
            try:
                await lock.async_acquire()
                wakeup_order.append("cancelled_async")  # Should not reach here
                lock.release()
            except asyncio.CancelledError:
                wakeup_order.append("async_cancelled")
                raise
        
        # Create second async waiter
        async def async_waiter2():
            await lock.async_acquire()
            wakeup_order.append("async2")
            lock.release()
        
        # Schedule async waiters
        task1 = asyncio.create_task(async_waiter1())
        await asyncio.sleep(0.1)
        
        cancel_task = asyncio.create_task(async_cancelled_waiter())
        await asyncio.sleep(0.1)
        
        task2 = asyncio.create_task(async_waiter2())
        await asyncio.sleep(0.1)
        
        # Cancel the task that should be cancelled
        cancel_task.cancel()
        
        # Release the lock, which should trigger the first waiter
        lock.release()
        
        # Wait for all operations to complete
        await asyncio.sleep(0.3)  # Give time for the timeout to occur
        await task1
        await task2
        
        try:
            await cancel_task
        except asyncio.CancelledError:
            pass
        
        self.assertTrue(sync_event.wait(timeout=1.0))
        self.assertTrue(timeout_event.wait(timeout=1.0))
        timeout_thread.join()
        sync_thread.join()
        
        # Check the wakeup order
        self.assertIn("sync", wakeup_order)
        self.assertIn("async1", wakeup_order)
        self.assertIn("async2", wakeup_order)
        self.assertIn("timeout_sync_failed", wakeup_order)
        self.assertIn("async_cancelled", wakeup_order)
        
        # Check the correct order of successful lock acquisitions
        acquisition_order = [item for item in wakeup_order if item in ["sync", "async1", "async2"]]
        self.assertEqual(acquisition_order, ["sync", "async1", "async2"])

if __name__ == '__main__':
    unittest.main()