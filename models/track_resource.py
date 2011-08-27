import logging
from hashlib import sha1
from task import Task

class TrackResource(Task):

    def __init__(self, tracker_id=None, *args, **kwargs):
        Task.__init__(self, *args, **kwargs)
        self.tracker_id = tracker_id
