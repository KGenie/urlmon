from services.storage import StorageService
from models.webpage import Webpage
from util import normalize_url

class WebpageService(StorageService):

    entity = Webpage

    @classmethod
    def get_by_url(self, url):
        return self.get(url)
