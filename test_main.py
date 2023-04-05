import threading
import time
from unittest import TestCase

from main import CacheServer


class TestCacheServer(TestCase):

    def setUp(self) -> None:
        self.cache_server = CacheServer()

    def test_get_not_existed_key(self):
        none_result = self.cache_server.get('abc')
        self.assertIsNone(none_result)

    def test_get_existed_key(self):
        self.cache_server.set(key='a', value='123', data_type='str')
        result = self.cache_server.get('a')
        self.assertEqual(result, '123')

    def test_get_expired_key(self):
        self.cache_server.set(key='a', value='123', data_type='str')
        time.sleep(6)
        result = self.cache_server.get('a')
        self.assertIsNone(result)

    def test_thread_safety(self):
        # Define a function that gets and sets a value in the cache server
        def get_and_set(i):
            self.cache_server.set(key="foo", value=f"bar_{i}", data_type="str")
            time.sleep(0.01)
            self.assertEqual(self.cache_server.get("foo"), f"bar_{i}")

        # Create multiple threads that call the get_and_set function
        threads = [threading.Thread(target=get_and_set, args=(i,)) for i in range(2)]
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
