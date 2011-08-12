from app_components.model import Model

class Resource(Model):

    def __init__(self, url, contents):
        self.url = url
        self.contents = contents
