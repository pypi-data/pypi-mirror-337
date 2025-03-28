import unittest
import asyncio
import threading
import time
import logging
from unittest.mock import patch

from pybatcher.batcher import Batcher
from pybatcher.exceptions import BatchNotReadyError

# Configure logging for tests
logging.basicConfig(level=logging.ERROR, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Configure specific logger levels
logging.getLogger('pybatcher.batch').setLevel(logging.INFO)
logging.getLogger('pybatcher.batcher').setLevel(logging.INFO)

# Logger for tests
test_logger = logging.getLogger("test")
logging.getLogger('test').setLevel(logging.INFO)


class TestBatcherInitialization(unittest.TestCase):
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
        
    def test_valid_initialization(self):
        """Test initialization with valid parameters."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, loop=self.loop)
        self.assertEqual(batcher.min_batch_size, 1)
        self.assertIsNone(batcher.max_batch_size)
        self.assertEqual(batcher.batch_delay, None)
        self.assertFalse(batcher.strict_batch_size)
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_invalid_batch_delay(self):
        """Test initialization with negative batch_delay."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        with self.assertRaises(ValueError):
            Batcher(lambda x: x, batch_delay=0, loop=self.loop)
        with self.assertRaises(ValueError):
            Batcher(lambda x: x, batch_delay=-1, loop=self.loop)
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
            
    def test_invalid_min_batch_size(self):
        """Test initialization with invalid min_batch_size."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        with self.assertRaises(ValueError):
            Batcher(lambda x: x, min_batch_size=0, loop=self.loop)
        with self.assertRaises(ValueError):
            Batcher(lambda x: x, min_batch_size=-1, loop=self.loop)
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
            
    def test_invalid_max_batch_size(self):
        """Test initialization with invalid max_batch_size."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        with self.assertRaises(ValueError):
            Batcher(lambda x: x, min_batch_size=5, max_batch_size=5, loop=self.loop)
        with self.assertRaises(ValueError):
            Batcher(lambda x: x, min_batch_size=10, max_batch_size=5, loop=self.loop)
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
    
    def test_auto_loop_creation(self):
        """Test that batcher creates its own loop when none is provided."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        with patch('pybatcher.batcher.asyncio.get_running_loop', side_effect=RuntimeError):
            batcher = Batcher(lambda x: x)
            self.assertIsNotNone(batcher.loop)
            self.assertIsNotNone(batcher.thread)
            batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatcherBasicFunctionality(unittest.TestCase):
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
        
    def test_submit_single_request(self):
        """Test submitting a single request."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: [i.upper() for i in x], loop=self.loop)
        future = batcher.submit_request("test")
        self.assertIsNotNone(batcher.current_batch)
        batcher.flush()
        self.assertEqual(future.result(), "TEST")
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_batch_creation(self):
        """Test batch creation when submitting requests."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, loop=self.loop)
        first_batch = batcher.current_batch  # Should be None initially
        self.assertIsNone(first_batch)
        
        batcher.submit_request("test1")
        second_batch = batcher.current_batch
        self.assertIsNotNone(second_batch)
        
        batcher.flush()  # Process and clear current batch
        self.assertIsNone(batcher.current_batch)
        
        batcher.submit_request("test2")
        third_batch = batcher.current_batch
        self.assertIsNotNone(third_batch)
        self.assertNotEqual(id(second_batch), id(third_batch))  # Should be a new batch
        
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_batch_transition_when_full(self):
        """Test that new batch is created when current batch is full."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, max_batch_size=2, loop=self.loop)
        
        future1 = batcher.submit_request("test1")
        future2 = batcher.submit_request("test2")
        first_batch = batcher.current_batch
        
        # Batch should be full and processed automatically
        self.assertTrue(first_batch.is_full())
        time.sleep(0.1)  # Give time for processing
        
        # Adding a new request should create a new batch
        future3 = batcher.submit_request("test3")
        self.assertNotEqual(id(first_batch), id(batcher.current_batch))
        
        batcher.close()
        
        # Check results
        self.assertEqual(future1.result(), "test1")
        self.assertEqual(future2.result(), "test2")
        self.assertEqual(future3.result(), "test3")
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatcherFlushBehavior(unittest.TestCase):
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
        
    def test_flush_ready_batch(self):
        """Test flush with a ready batch."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, loop=self.loop)
        future = batcher.submit_request("test")
        
        # Batch should be ready with one request (min_batch_size=1 by default)
        self.assertTrue(batcher.current_batch.ready())
        
        batcher.flush()
        time.sleep(0.1)  # Give time for processing
        
        # Batch should be processed and future should be resolved
        self.assertTrue(future.done())
        self.assertEqual(future.result(), "test")
        self.assertIsNone(batcher.current_batch)  # Current batch should be cleared
        
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_flush_not_ready_batch(self):
        """Test flush with a batch that's not ready."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, min_batch_size=2, loop=self.loop)
        future = batcher.submit_request("test")
        
        # Batch should not be ready with one request (min_batch_size=2)
        self.assertFalse(batcher.current_batch.ready())
        with self.assertRaises(BatchNotReadyError):
            batcher.flush()
        time.sleep(0.1)
        
        # Batch should not be processed
        self.assertFalse(future.done())
        self.assertIsNotNone(batcher.current_batch)  # Current batch should still exist
        
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatcherAsyncFunctionality(unittest.TestCase):
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
        
    def test_handle_request(self):
        """Test async handle_request method."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: [i.upper() for i in x])

        async def run_test():
            result = await batcher.handle_request("test")
            self.assertEqual(result, "TEST")
        
        future = asyncio.run_coroutine_threadsafe(run_test(), self.loop)
        time.sleep(0.1) # Give time for starting the coroutine
        batcher.flush()
        future.result(timeout=1.0)
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_async_process_function(self):
        """Test batcher with async process function."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        async def async_process(items):
            await asyncio.sleep(0.1)
            return [i.upper() for i in items]
            
        batcher = Batcher(async_process, loop=self.loop)
        future = batcher.submit_request("test")
        batcher.flush()
        result = future.result(timeout=1.0)
        self.assertEqual(result, "TEST")
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatcherTiming(unittest.TestCase):
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
        
    def test_auto_batch_processing_after_delay(self):
        """Test that batch is processed automatically after delay."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, batch_delay=0.1, loop=self.loop)
        future = batcher.submit_request("test")
        
        # Wait for auto-processing
        time.sleep(0.5)
        
        self.assertTrue(future.done() or future.running())
        self.assertEqual(future.result(), "test")
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_immediate_batch_processing_when_full(self):
        """Test that batch is processed immediately when full."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, max_batch_size=2, loop=self.loop)
        future1 = batcher.submit_request("test1")
        future2 = batcher.submit_request("test2")
        
        # Wait for auto-processing
        time.sleep(0.1)
        
        self.assertTrue(future1.done())
        self.assertTrue(future2.done())
        self.assertEqual(future1.result(), "test1")
        self.assertEqual(future2.result(), "test2")
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatcherResourceManagement(unittest.TestCase):
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
        
    def test_close_with_pending_batch(self):
        """Test close() with pending batch."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, loop=self.loop)
        future = batcher.submit_request("test")

        # Close with pending batch
        batcher.close()
        
        # Future should be resolved or running
        self.assertTrue(future.done() or future.running())
        self.assertEqual(future.result(), "test")
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    @patch('pybatcher.batcher.asyncio.get_running_loop', side_effect=RuntimeError)
    def test_internal_loop_cleanup(self, mock_get_loop):
        """Test cleanup of internally created loop."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x)
        self.assertIsNotNone(batcher.thread)
        self.assertIsNotNone(batcher.loop)
        
        batcher.close()
        time.sleep(0.1)  # Give time for thread to join
        
        # Thread should have been stopped
        self.assertFalse(batcher.thread.is_alive())
        self.assertTrue(batcher.loop.is_closed())
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatcherConcurrency(unittest.TestCase):
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
        
    def test_multiple_concurrent_requests(self):
        """Test submitting multiple concurrent requests."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: [i.upper() for i in x], max_batch_size=5, loop=self.loop)
        
        # Submit multiple requests concurrently
        futures = []
        for i in range(10):
            futures.append(batcher.submit_request(f"test{i}"))
            
        # Wait for processing to complete
        time.sleep(0.2)
        
        # Verify all requests were processed
        for i, future in enumerate(futures):
            self.assertTrue(future.done())
            self.assertEqual(future.result(), f"TEST{i}")
            
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_thread_safety(self):
        """Test thread safety of submit_request."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: [i.upper() for i in x], max_batch_size=50, loop=self.loop)
        futures = []
        
        def submit_requests():
            for i in range(10):
                futures.append(batcher.submit_request(f"thread{i}"))
                
        # Start multiple threads submitting requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=submit_requests)
            thread.start()
            threads.append(thread)
            
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        # Wait for processing to complete
        futures[0].result()

        # Verify all requests were processed
        self.assertEqual(len(futures), 50)
        for future in futures:
            self.assertTrue(future.done())
            self.assertTrue(future.result().startswith("THREAD"))
        
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


class TestBatcherErrorHandling(unittest.TestCase):
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
        
    def test_exception_in_processing(self):
        """Test exception in processing function."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        def failing_process(items):
            raise ValueError("Test error")
            
        batcher = Batcher(failing_process, loop=self.loop)
        future = batcher.submit_request("test")
        batcher.flush()
        
        with self.assertRaises(ValueError):
            future.result()
            
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")
        
    def test_strict_size_behavior(self):
        """Test behavior with strict_batch_size=True."""
        test_logger.info(f"RUNNING TEST: {self._testMethodName}")
        batcher = Batcher(lambda x: x, min_batch_size=3, strict_batch_size=True, loop=self.loop)
        
        # Add requests
        future1 = batcher.submit_request("test1")
        future2 = batcher.submit_request("test2")
        future3 = batcher.submit_request("test3")
        
        # With 3 requests, batch is ready
        self.assertTrue(batcher.current_batch.ready())
        
        # Cancel one request
        future1.cancel()
        
        # With strict_size=True and one cancelled request, batch is no longer ready
        self.assertFalse(batcher.current_batch.ready())
        
        # Add another request to make it ready again
        future4 = batcher.submit_request("test4")
        self.assertTrue(batcher.current_batch.ready())
        
        batcher.flush()
        time.sleep(0.1)
        
        self.assertTrue(future2.done())
        self.assertTrue(future3.done())
        self.assertTrue(future4.done())
        
        batcher.close()
        test_logger.info(f"COMPLETED TEST: {self._testMethodName}")


if __name__ == '__main__':
    test_logger.info("=" * 70)
    test_logger.info("STARTING BATCHER TESTS")
    test_logger.info("=" * 70)
    unittest.main()
    test_logger.info("=" * 70)
    test_logger.info("COMPLETED BATCHER TESTS")
    test_logger.info("=" * 70)
