from datetime import datetime
from app_components.model import Model
from util import normalize_url


class Webpage(Model):
    
        def __init__(self, url, last_checked=datetime.min):
            self.url = url
            self.last_checked = last_checked


        @property
        def url(self):
            return self._url


        @url.setter
        def url(self, value):
            self._url = normalize_url(value)
