import datetime
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass

EXPIRATION_MS: [str, float] = {
    'css': 1000,
    'html': 2000,
    'json': 4000,
    'str': 5000
}


@dataclass
class CacheItem:
    value: str
    data_type: str
    init_time: datetime = datetime.datetime.now()


class CacheServer:
    def __init__(self, max_size: int = 1024):
        # use OrderedDict to implement LRU
        self.cache = OrderedDict()
        self.max_size = max_size
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            cache_item: CacheItem = self.cache.get(key)
            if cache_item:
                lifetime = datetime.datetime.now() - cache_item.init_time
                if lifetime.total_seconds() * 1000 < EXPIRATION_MS[cache_item.data_type]:
                    # keep the recently used item in the end
                    self.cache.move_to_end(key)
                    return cache_item.value
                else:
                    del self.cache[key]
            return None

    def set(self, key, value, data_type):
        with self.lock:
            # check the size of current cache server
            self.check_cache_size()

            cache_item = CacheItem(value, data_type)
            self.cache[key] = cache_item

    def check_cache_size(self):
        """clean items by LRU, removed the first element in the dictionary"""
        while len(self.cache) > self.max_size:
            self.cache.popitem(last=False)


if __name__ == '__main__':
    cache_server = CacheServer()
    cache_server.set(key='a', value='123', data_type='str')
    print('Example of existed key: ', cache_server.get('a'))
    time.sleep(4)
    print('Example of existed key within expiration time: ', cache_server.get('a'))
    time.sleep(1.1)
    print('Example of existed key after expiration time: ', cache_server.get('a'))

    print('Example of non existed key: ', cache_server.get('b'))
