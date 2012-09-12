#coding=:utf-8
from gevent.coros import BoundedSemaphore

class Cache(dict):

    semaphore = BoundedSemaphore()

    def __setattr__(self, key, value): 
        with self.semaphore:
            self[key] = value
    
    def __delattr__(self, key):
        with self.semaphore:
            try:
                del self[key]
            except KeyError, k:
                raise AttributeError, k


online_cache = Cache()
user_cache = Cache()