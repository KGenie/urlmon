from app_components.model import Model
from hashlib import sha1
from util import normalize_url

class Webpage(Model):
    
    def __init__(self, url, contents, last_modified):
        self.id = None
        self.url = url
        self.contents = contents
        self.last_modified = last_modified

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = normalize_url(value)
       
    @property
    def contents(self):
        return self._contents


    @contents.setter
    def contents(self, value):
        h = sha1()
        h.update(value)
        self.digest = h.hexdigest()        
        self._contents = value
