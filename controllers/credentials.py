from app_components.controller import WebMonitorController
from wtforms.validators import ValidationError
from wsgi.auth import auth
from wsgi.http_method import get, post
from forms.login import LoginForm
from models.user import User
from services.user import UserService

@auth(required=False)
class CredentialsController(WebMonitorController):

    user_service = UserService

    @post
    def login(self, request):
        form = LoginForm(request.POST)
        redirect_controller = self.request.GET.get('rc',None) or 'home'
        redirect_action = self.request.GET.get('ra',None) or 'main'

        user = User()
        form.populate_obj(user)
        user = self.user_service.authenticate(user)

        def fail_validator(x,y): 
            raise ValidationError('Invalid email or password')

        if not user:
            form._fields['password'].validators.append(fail_validator)

        if form.validate():
            self.session['user'] = user
            return self.redirect(redirect_action, redirect_controller)
        else:
            model=dict(login_form=form, redirect_action=redirect_action,
                    redirect_controller=redirect_controller)
            return self.view(model, name='main', controller='home')

    @post
    def logout(self, request):
        redirect_controller = self.request.GET['rc']
        redirect_action = self.request.GET['ra']
        self.session['user'] = None
        return self.redirect(redirect_action, redirect_controller)
