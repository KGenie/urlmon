'''
26-Apr-2012,Andy:    Reconstruct URL here and pass to service (Registration)
'''

import util
from app_components.controller import WebMonitorController
from wsgi.auth import auth
from wsgi.http_method import get, post
from wtforms.validators import ValidationError
from forms.registration import RegistrationForm
from helpers import menu, UrlHelper
from models.user import User
from services.registration import RegistrationService
from services.user import UserService

@auth(required=False)
class RegistrationController(WebMonitorController):

    registration_service = RegistrationService
    user_service = UserService


    @menu(exclude=True)
    @get
    def new(self, request):
        form = RegistrationForm()
        return self.view(dict(form=form))


    @post
    def request_account(self, request):
        form = RegistrationForm(request.POST)
        setattr(form, '_user_service', self.user_service)
        setattr(form, '_registration_service', self.registration_service)

        if form.validate():
            user = User()
            form.populate_obj(user)
            my_url = util.reconstruct_url(self.context.environ)
            self.registration_service.request_registration(user,my_url)
            return self.redirect(controller='home', action='main')
        else:
            return self.view({'form': form}, 'new')


    @menu(exclude=True)
    @get
    def confirm_activation(self, request):
        reg_id = request.GET.get('reg_id', None)
        return self.view({'reg_id': reg_id})


    @post
    def activate(self, request):
        reg_id = request.POST.get('reg_id', None)
        my_url = util.reconstruct_url(self.context.environ)
        if reg_id:
            user = self.registration_service.activate_user(reg_id, my_url)
            if user:
                self.session['user'] = user
                return self.redirect('main', 'home')
        raise Exception('User couldn\'t be activated!')
