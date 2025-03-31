from functools import lru_cache

def cached(func):
    return lru_cache(maxsize=100)(func)