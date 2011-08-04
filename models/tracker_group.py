from app_components.model import Model

class TrackerGroup(Model):

    def __init__(self, name=None, comment=None, user=None):
        self.name = name
        self.comment = comment
        self.user = user
