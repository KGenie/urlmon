from app_components.controller import WebMonitorController
from wtforms.validators import ValidationError
from wsgi.auth import auth
from wsgi.http_method import get, post
from forms.login import LoginForm
from models.user import User
from services.user import UserService
from services.registration import RegistrationService
from database.sqlalch import Session

@auth(required=False)
class CredentialsController(WebMonitorController):

    user_service = UserService
    registration_service = RegistrationService

    @post
    def login(self, request):
        form = LoginForm(request.POST)
        redirect_controller = self.request.GET.get('rc',None) or 'tracker_change'
        redirect_action = self.request.GET.get('ra',None) or 'index'
        id = self.request.GET.get('id',None)
        qsargs = {}
        if id:
            qsargs['id'] = id

        setattr(form, '_user_service', self.user_service)
        setattr(form, '_registration_service', self.registration_service)

        if form.validate():
            user = form._user
            self.session['user'] = user
            return self.redirect(redirect_action, redirect_controller, **qsargs)
        else:
            model=dict(login_form=form, redirect_action=redirect_action,
                    redirect_controller=redirect_controller, **qsargs)
            return self.view(model, name='main', controller='home')

    @post
    def logout(self, request):
        self.session['user'] = None
        return self.redirect_url('/')
