from app_components.controller import WebMonitorController
from wsgi.auth import auth
from wsgi.http_method import get
from helpers import menu


@auth(required=False)
class JsController(WebMonitorController):

    @get
    @menu(exclude=True)
    def helpers(self, request):
        return self.js()
        
