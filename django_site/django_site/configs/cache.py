from ..settings import MIDDLEWARE


MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    *MIDDLEWARE,
    'django.middleware.cache.FetchFromCacheMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60,
    }
}

CACHE_MIDDLEWARE_ALIAS      = 'default'   # 采用哪个缓存
CACHE_MIDDLEWARE_SECONDS    = 60         # 每个页面的缓存超时时间
CACHE_MIDDLEWARE_KEY_PREFIX = ''
