from app_components.controller import WebMonitorController
from models.user import User
from forms.user import UserForm
from services.user import UserService
from wsgi.http_method import get, post
from wsgi.auth import auth
from helpers import menu

@menu(label='User Settings')
@auth(allow=('admin',))
class UserController(WebMonitorController):

    user_service = UserService

    @get
    @menu(label='View registered users')
    def index(self, request):
        form = UserForm()
        users = self.user_service.get_all()

        return self.view({'form': form, 'users': users})
