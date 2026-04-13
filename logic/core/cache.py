_cache = {}


def get_cache(key, loader_fn):
    if key not in _cache:
        _cache[key] = loader_fn()
    return _cache[key]


def clear_cache(key=None):
    if key:
        _cache.pop(key, None)
    else:
        _cache.clear()
