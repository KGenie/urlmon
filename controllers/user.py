from app_components.controller import WebMonitorController
from models.user import User, UserTable
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
    @menu(label='Registered users')
    def index(self, request):
        users = self.user_service.get_all()
        table_model = UserTable(users)

        return self.view({'table_model': table_model})
