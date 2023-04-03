import datetime
import time
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


@dataclass
class CacheServer:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        cache_item: CacheItem = self.cache.get(key)
        if cache_item:
            lifetime = datetime.datetime.now() - cache_item.init_time
            if lifetime.total_seconds() * 1000 < EXPIRATION_MS[cache_item.data_type]:
                return cache_item.value
        return None

    def set(self, key, value, data_type):
        cache_item = CacheItem(value, data_type)
        self.cache[key] = cache_item


if __name__ == '__main__':
    cache_server = CacheServer()
    cache_server.set(key='a', value='123', data_type='str')
    print('Example of existed key: ', cache_server.get('a'))
    time.sleep(4)
    print('Example of existed key within expiration time: ', cache_server.get('a'))
    time.sleep(1.1)
    print('Example of existed key after expiration time: ', cache_server.get('a'))

    print('Example of non existed key: ', cache_server.get('b'))
