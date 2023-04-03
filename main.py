class CacheServer:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value


if __name__ == '__main__':
    cache_server = CacheServer()
    cache_server.set('a', 123)
    print('Example of existed key: ', cache_server.get('a'))
    print('Example of non existed key: ', cache_server.get('b'))
