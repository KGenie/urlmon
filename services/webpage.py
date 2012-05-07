import string
from services.storage import StorageService
from models.webpage import Webpage
from util import normalize_url

class WebpageService(StorageService):

    entity = Webpage

    def get_by_url(self, url):
        return self.get(url)
    
    def insert(self,webpage):
        webpage.url = self.tidy_url(webpage.url)
        webpage = super(WebpageService, self).insert(webpage)
        
    def tidy_url (self,arg_url):
        print "tidy"
        http_regular = "http://"
        after_regular = 7
        http_secure = "https://"
        after_secure = 8
            
        my_url = normalize_url(arg_url)
# Is it HTTPS?
        is_secure = my_url.startswith(http_secure)
        
# Remove ALL leading HTTP*://. Renormalising addresses any case issues
        my_more = -1
        while my_more:
            print my_url + "!!"
            my_more = 0
            if my_url[:after_regular].lower() == http_regular:
                my_more = 1
                my_url = my_url[after_regular:]
            if my_url[:after_secure].lower() == http_secure:
                my_more = 1
                my_url = my_url[after_secure:]
            
        my_url = my_url.lstrip(http_regular)
        my_url = my_url.lstrip(http_secure)
# And again
        my_url = my_url.lstrip(http_regular)
        my_url = my_url.lstrip(http_secure)
# Put ONE http back
        if is_secure:
            my_url = http_secure + my_url
        else:
            my_url = http_regular + my_url

        return my_url

    
    
