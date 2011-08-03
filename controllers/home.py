from app_components.controller import WebMonitorController
from wsgi.auth import auth
from wsgi.http_method import get
from forms.login import LoginForm


@auth(required=False)
class HomeController(WebMonitorController):

    @get
    def main(self, request):
        model = {}
        redirect_controller = self.request.GET.get('rc', None)
        redirect_action = self.request.GET.get('ra', None)
        if redirect_controller:
            model['redirect_controller'] = redirect_controller
        if redirect_action:
            model['redirect_action'] = redirect_action
        model['login_form'] = LoginForm()
        return self.view(model)
