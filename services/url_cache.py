from app_components.service import Service
from daemons.url_cache import cache_url_async

class UrlCacheService(Service):

    def cache_url(self, url):
        cache_url_async(url)
