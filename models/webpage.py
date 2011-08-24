from datetime import datetime, timedelta
from app_components.model import Model
from hashlib import sha1
from util import normalize_url


class Webpage(Model):
    
        def __init__(self, url, contents=None, last_updated=datetime.min):
            self.url = url
            self.contents = contents
            self.last_updated = last_updated


        @property
        def url(self):
            return self._url


        @url.setter
        def url(self, value):
            self._url = normalize_url(value)
           

        @property
        def contents(self):
            return self._contents.decode('utf-8')


        @contents.setter
        def contents(self, value):
            h = sha1()
            if isinstance(value, unicode):
                h.update(value.encode('utf-8'))
            elif isinstance(value, str):
                h.update(value)
            self.digest = h.digest()        
            self._contents = value
