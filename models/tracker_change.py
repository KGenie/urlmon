from hashlib import sha1
from app_components.model import Model

class TrackerChange(Model):

    def __init__(self, tracker_id=None, webpage_version_id=None, content='',
            start_index=0, current_css_selector=None):
        self.tracker_id = tracker_id
        self.webpage_version_id = webpage_version_id
        self.content = content
        self.start_index = start_index
        self.current_css_selector = current_css_selector


    @property
    def content(self):
        return self._content.decode('utf-8')


    @content.setter
    def content(self, value):
        h = sha1()
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        h.update(value)
        self.digest = h.digest()        
        self._content = value
