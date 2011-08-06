from app_components.model import Model

class TrackerGroup(Model):

    def __init__(self, id=None, name=None, comment=None, user=None):
        self.id = id
        self.name = name
        self.comment = comment
        self.user = user
