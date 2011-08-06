from app_components.model import Model

class Tracker(Model):

    def __init__(self, id=None, name=None, url=None, frequency=None, 
            tracker_group=None, user=None):
        self.id = id
        self.name = name
        self.url = url
        self.frequency = frequency
        self.tracker_group = tracker_group
        self.user = user
