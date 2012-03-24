from app_components.service import Service
from daemons.webpage import DAEMON as fetcher_daemon


class FetcherService(Service):

    def fetch(self, url, selector):
        return fetcher_daemon.fetch(url, selector)
