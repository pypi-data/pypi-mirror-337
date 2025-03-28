import unittest
import asyncio
import threading
import time
import logging
from concurrent.futures import CancelledError, TimeoutError

from pybatcher.batch import Batch
from pybatcher.exceptions import FullBatchError

# Configure logging for tests
logging.basicConfig(level=logging.ERROR, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Set pybatcher.batch logger to INFO level
logging.getLogger('pybatcher.batch').setLevel(logging.INFO)

# Logger for tests
test_logger = logging.getLogger("test")
logging.getLogger('test').setLevel(logging.INFO)


class TestBatchInitialization(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        def _run_loop():
            self.loop.run_forever()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_default_initialization(self):
        """Test initialization with default parameters."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batch = Batch(lambda x: x)
        self.assertEqual(batch.min_size, 1)
        self.assertIsNone(batch.max_size)
        self.assertIsNone(batch.auto_start_delay)
        self.assertFalse(batch.start_when_full)
        self.assertTrue(batch.is_empty())
        self.assertFalse(batch.is_full())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_min_size_zero(self):
        """Test initialization with min_size=0."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batch = Batch(lambda x: x, min_size=0)
        self.assertEqual(batch.min_size, 0)
        self.assertTrue(batch.ready())  # Should be ready immediately with min_size=0
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_max_size_specified(self):
        """Test initialization with max_size specified."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batch = Batch(lambda x: x, max_size=10)
        self.assertEqual(batch.max_size, 10)
        self.assertFalse(batch.is_full())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_auto_start_parameters(self):
        """Test initialization with auto-start parameters."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batch = Batch(lambda x: x, max_size=5, auto_start_delay=1.0, auto_start_when_full=True)
        self.assertEqual(batch.auto_start_delay, 1.0)
        self.assertTrue(batch.start_when_full)
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatchAddRequest(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        def _run_loop():
            self.loop.run_forever()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_add_request(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test adding a request to the batch."""
        batch = Batch(lambda x: x)
        future = batch.add_request("test")
        self.assertEqual(len(batch.requests), 1)
        self.assertFalse(future.done())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_add_request_to_full_batch(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test adding a request to a full batch."""
        batch = Batch(lambda x: x, max_size=1)
        batch.add_request("test")
        with self.assertRaises(FullBatchError):
            batch.add_request("test2")
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_add_request_to_started_batch(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test adding a request to a started batch."""
        batch = Batch(lambda x: x)
        batch.add_request("test")
        batch.start()
        with self.assertRaises(RuntimeError):
            batch.add_request("test2")
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatchState(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        def _run_loop():
            self.loop.run_forever()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_ready_state(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test the ready state of a batch."""
        # Batch with min_size=2
        batch = Batch(lambda x: x, min_size=2)
        self.assertFalse(batch.ready())
        batch.add_request("test1")
        self.assertFalse(batch.ready())
        batch.add_request("test2")
        self.assertTrue(batch.ready())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_started_state(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test the started state of a batch."""
        batch = Batch(lambda x: x)
        self.assertFalse(batch.started())
        batch.add_request("test")
        batch.start()
        self.assertTrue(batch.started())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_running_state(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test the running state of a batch."""
        def slow_process(data):
            time.sleep(0.1)
            return data
            
        batch = Batch(slow_process)
        self.assertFalse(batch.running())
        batch.add_request("test")
        batch.start()
        self.assertTrue(batch.running())
        # Wait for the process to complete
        time.sleep(0.2)
        self.assertFalse(batch.running())
        self.assertTrue(batch.done())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_is_full(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test the is_full method."""
        batch = Batch(lambda x: x, max_size=2)
        self.assertFalse(batch.is_full())
        batch.add_request("test1")
        self.assertFalse(batch.is_full())
        batch.add_request("test2")
        self.assertTrue(batch.is_full())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_is_empty(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test the is_empty method."""
        batch = Batch(lambda x: x)
        self.assertTrue(batch.is_empty())
        batch.add_request("test")
        self.assertFalse(batch.is_empty())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_can_add_request(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test the can_add_request method."""
        batch = Batch(lambda x: x, max_size=1)
        self.assertTrue(batch.can_add_request())
        batch.add_request("test")
        self.assertFalse(batch.can_add_request())  # Full

        batch = Batch(lambda x: x)
        batch.add_request("test")
        batch.start()
        self.assertFalse(batch.can_add_request())  # Started
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestAutoStart(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        started_event = threading.Event()
        def _run_loop():
            test_logger.info("Starting loop")
            self.loop.run_forever()
            test_logger.info("Loop stopped")
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        self.loop.call_soon_threadsafe(
            started_event.set)
        started_event.wait()
        test_logger.info("Loop started")
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_auto_start_delay(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test auto start after delay."""
        batch = Batch(lambda x: x, auto_start_delay=0.1)
        batch.add_request("test")
        self.assertIsNotNone(batch.timer)
        time.sleep(0.5)  # Wait for auto start
        self.assertTrue(batch.started() or batch.done())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_auto_start_when_full(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test auto start when batch is full."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_test():
            batch = Batch(lambda x: x, max_size=2, auto_start_when_full=True, loop=loop)
            future1 = batch.add_request("test1")
            self.assertFalse(batch.started())
            future2 = batch.add_request("test2")  # Should trigger auto start
            
            # Give time for the auto-start to occur
            await asyncio.sleep(0.1)
            self.assertTrue(batch.started() or batch.done())
            
            # Wait for results
            await asyncio.gather(asyncio.wrap_future(future1), asyncio.wrap_future(future2))
            
        loop.run_until_complete(run_test())
        loop.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatchProcessing(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        def _run_loop():
            self.loop.run_forever()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_sync_processing(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test synchronous processing function."""
        def process_func(items):
            return [item.upper() for item in items]
            
        batch = Batch(process_func)
        future1 = batch.add_request("test1")
        future2 = batch.add_request("test2")
        batch.start()
        
        # Wait for processing to complete
        time.sleep(0.1)
        
        self.assertEqual(future1.result(), "TEST1")
        self.assertEqual(future2.result(), "TEST2")
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_async_processing(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test asynchronous processing function."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def process_func(items):
            await asyncio.sleep(0.1)
            return [item.upper() for item in items]
            
        async def run_test():
            batch = Batch(process_func, loop=loop)
            future1 = batch.add_request("test1")
            future2 = batch.add_request("test2")
            batch.start(blocking=False)
            
            # Wait for futures
            results = await asyncio.gather(asyncio.wrap_future(future1), asyncio.wrap_future(future2))
            self.assertEqual(results, ["TEST1", "TEST2"])
            
        loop.run_until_complete(run_test())
        loop.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_exception_in_processing(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test exception in processing function."""
        def failing_process(items):
            raise ValueError("Test error")
            
        batch = Batch(failing_process)
        future = batch.add_request("test")
        batch.start()
        
        time.sleep(0.1)  # Wait for processing
        
        with self.assertRaises(ValueError):
            future.result()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatchResults(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        def _run_loop():
            self.loop.run_forever()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_results_with_timeout(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test getting results with timeout."""
        def slow_process(items):
            time.sleep(0.2)
            return items
            
        batch = Batch(slow_process)
        batch.add_request("test")
        batch.start()
        
        # Timeout too short
        with self.assertRaises(TimeoutError):
            batch.results(timeout=0.1)
            
        # Sufficient timeout
        results = batch.results(timeout=0.3)
        self.assertEqual(results, ["test"])
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_cancelled_batch_results(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test getting results from cancelled batch."""
        batch = Batch(lambda x: x)
        batch.add_request("test")
        self.assertTrue(batch.cancel(), "Batch should be cancelled")
        self.assertTrue(batch.cancelled(), "Batch should have been cancelled")
        with self.assertRaises(CancelledError):
            batch.results()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatchCancellation(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        def _run_loop():
            self.loop.run_forever()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_cancel_before_start(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test cancelling batch before start."""
        batch = Batch(lambda x: x)
        future = batch.add_request("test")
        self.assertTrue(batch.cancel())
        self.assertTrue(batch.cancelled())
        self.assertTrue(future.cancelled())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_cancel_after_start(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test cancelling batch after start."""
        batch = Batch(lambda x: x)
        batch.add_request("test")
        batch.start()
        self.assertFalse(batch.cancel())  # Can't cancel after start
        self.assertFalse(batch.cancelled())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestStrictSize(unittest.TestCase):
    def setUp(self):
        test_logger.info("=" * 70)
        test_logger.info(f"SETTING UP: {self.__class__.__name__}")
        def _run_loop():
            self.loop.run_forever()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=_run_loop)
        self.thread.daemon = True
        self.thread.start()
        asyncio.set_event_loop(self.loop)
        
    def tearDown(self):
        test_logger.info(f"TEARING DOWN: {self.__class__.__name__}")
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()
        asyncio.set_event_loop(None)
    
    def test_length_with_strict_size(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test batch length calculation with strict_size=True vs False."""
        # With strict_size=False (default)
        batch_default = Batch(lambda x: x, max_size=3)
        futures = [batch_default.add_request(i) for i in range(3)]
        self.assertEqual(len(batch_default), 3)
        
        # Complete one request
        futures[0].cancel()
        self.assertEqual(len(batch_default), 3)  # Still counts completed requests
        
        # With strict_size=True
        batch_strict = Batch(lambda x: x, max_size=3, strict_size=True)
        futures = [batch_strict.add_request(i) for i in range(3)]
        self.assertEqual(len(batch_strict), 3)
        
        # Complete one request
        futures[0].cancel()
        self.assertEqual(len(batch_strict), 2)  # Doesn't count completed requests
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_is_full_with_strict_size(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test is_full behavior with strict_size=True."""
        # With strict_size=False (default)
        batch_default = Batch(lambda x: x, max_size=3)
        futures = [batch_default.add_request(i) for i in range(3)]
        self.assertTrue(batch_default.is_full())
        
        # Complete one request - still full with default behavior
        futures[0].cancel()
        self.assertTrue(batch_default.is_full())
        
        # With strict_size=True
        batch_strict = Batch(lambda x: x, max_size=3, strict_size=True)
        futures = [batch_strict.add_request(i) for i in range(3)]
        self.assertTrue(batch_strict.is_full())
        
        # Complete one request - no longer full with strict_size=True
        futures[0].cancel()
        self.assertFalse(batch_strict.is_full())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_ready_with_strict_size(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test ready behavior with strict_size=True."""
        # With strict_size=False (default)
        batch_default = Batch(lambda x: x, min_size=3)
        futures = [batch_default.add_request(i) for i in range(3)]
        self.assertTrue(batch_default.ready())
        
        # Complete one request - still ready with default behavior
        futures[0].cancel()
        self.assertTrue(batch_default.ready())
        
        # With strict_size=True
        batch_strict = Batch(lambda x: x, min_size=3, strict_size=True)
        futures = [batch_strict.add_request(i) for i in range(3)]
        self.assertTrue(batch_strict.ready())
        
        # Complete one request - no longer ready with strict_size=True
        futures[0].cancel()
        self.assertFalse(batch_strict.ready())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")

    def test_can_add_after_completion_with_strict_size(self):
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        """Test ability to add requests after some complete with strict_size=True."""
        # With strict_size=False (default)
        batch_default = Batch(lambda x: x, max_size=3)
        futures = [batch_default.add_request(i) for i in range(3)]
        
        # Complete one request - still can't add with default behavior
        futures[0].cancel()
        self.assertFalse(batch_default.can_add_request())
        
        # With strict_size=True
        batch_strict = Batch(lambda x: x, max_size=3, strict_size=True)
        futures = [batch_strict.add_request(i) for i in range(3)]
        
        # Complete one request - now can add more with strict_size=True
        futures[0].cancel()
        self.assertTrue(batch_strict.can_add_request())
        
        # Add another request after completion
        _ = batch_strict.add_request(3)
        self.assertEqual(len(batch_strict), 3)  # Back to max size
        self.assertTrue(batch_strict.is_full())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


if __name__ == '__main__':
    test_logger.info("=" * 70)
    test_logger.info("STARTING BATCH TESTS")
    test_logger.info("=" * 70)
    unittest.main()
    test_logger.info("=" * 70)
    test_logger.info("COMPLETED BATCH TESTS")
    test_logger.info("=" * 70)
