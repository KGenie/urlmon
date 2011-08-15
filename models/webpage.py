from app_components.model import Model

class Webpage(Model):
    
    def __init__(self, url, contents, last_modified):
        self.id = None
        self.url = url
        self.contents = contents
        self.last_modified = last_modified
