from app_components.model import Model
from hashlib import sha1
from util import normalize_url


class WebpageVersion(Model):
    
        def __init__(self, url, content=None, date=None):
            self.url = url
            self.content = content
            self.date = date


        @property
        def url(self):
            return self._url


        @url.setter
        def url(self, value):
            self._url = normalize_url(value)
           

        @property
        def content(self):
            return self._content.decode('utf-8')


        @content.setter
        def content(self, value):
            h = sha1()
            if isinstance(value, unicode):
                h.update(value.encode('utf-8'))
            elif isinstance(value, str):
                h.update(value)
            self.digest = h.digest()        
            self._content = value
