import logging
from hashlib import sha1
from task import Task

class TrackResource(Task):

    def __init__(self, tracker_id=None, last_content='', *args, **kwargs):
        Task.__init__(self, *args, **kwargs)
        self.tracker_id = tracker_id
        self.last_content = last_content

    @property
    def last_content(self):
        return self._last_content.decode('utf-8')


    @last_content.setter
    def last_content(self, value):
        h = sha1()
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        h.update(value)
        self.last_digest = h.hexdigest()        
        self._last_content = value
