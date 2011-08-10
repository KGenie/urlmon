from app_components.service import Service
from daemons.url_cache import start_retrieving_url, finish_retrieving_url

class UrlCacheService(Service):

    def cache_url_contents(self, url):
        start_retrieving_url(url)


    def get_url_contents(self, url):
        return finish_retrieving_url(url)
