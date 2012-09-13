#coding=:utf-8
from gevent.coros import BoundedSemaphore
import hashlib
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

nas_cache = Cache()

stat_cache = Cache()

_cache = Cache()

def cache_data(category='all'):
    def func_warp1(func):
        def func_wrap2(*args, **kargs):
            sig = _mk_cache_sig(*args, **kargs)
            key = "%s:%s:%s"%(category,func.__name__, sig)
            data = _cache.get(key)
            if data is not None:
                return data
            data = func(*args, **kargs)
            if data is not None:
                _cache[key] = data
            return data
        return func_wrap2
    return func_warp1

def _mk_cache_sig(*args, **kargs):
    src_data = repr(args) + repr(kargs)
    m = hashlib.md5(src_data)
    sig = m.hexdigest()
    return sig


 