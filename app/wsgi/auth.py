from inspect import isclass
from services.user import UserService
from app_components.controller import WebMonitorController
from app_components.response import RedirectToLoginResponse, NotAuthorizedResponse
from util import get_controller_actions, is_authorized
from services.user import UserService


class AuthMiddleware(object):
    """
    Authentication/Authorization Middleware.

    This middleware will restrict access to controller actions based on
    settings defined by the 'auth' decorator. This decorator will be applied
    either explicitly in each of the controllers/actions or implicitly by
    using the options defined in the middleware initializer.
    """

    def __init__(self, app, login_controller='login',login_action='sign_in'):
        self.app = app
        self.login_controller = login_controller
        self.login_action = login_action


    def authorized(self, user, action_callable):
        user_roles = user.roles
        authorized_roles = action_callable._roles_allowed
        denied_roles = action_callable._roles_denied
        return is_authorized(user_roles, authorized_roles, denied_roles)


    def __call__(self, environ, start_response):
        request = environ['request']
        controller_class = environ['route']['controller_class']
        action_callable = environ['route']['action_callable']
        session = environ['beaker.session']

        user = session.get('user', None)
        if not user:
            # TODO Remove this when not developing
            user = UserService(None).get_all().next()
            session['user'] = user

        if action_callable._authentication_required:
            if not user:
                controller = environ['route']['controller']
                action = environ['route']['action']
                qsargs={'rc':controller,'ra':action }
                id = request.GET.get('id', None)
                if id:
                    qsargs['id'] = id
                return RedirectToLoginResponse(controller=self.login_controller,\
                        action=self.login_action,qsargs=qsargs)
            elif not self.authorized(user, action_callable):
                return NotAuthorizedResponse()

        return self.app(environ, start_response)

class auth(object):
    """
    Authentication/Authorization decorator.

    This decorator can be applied to controllers/actions to setup access 
    control. When applied to a controller, all actions that have not
    been decorated will inherit it's controller access control settings.
    """
    allow_key = '_roles_allowed'
    deny_key = '_roles_denied'
    required_key = '_authentication_required'

    def __init__(self,required=None, allow=None, deny=None):
        if required is not None:
            self.required = required
        if allow is not None:
            self.allow = set(allow)
        if deny is not None:
            self.deny = set(deny)

    def __call__(self, controller_or_action):
        allow_key = self.allow_key
        deny_key = self.deny_key
        required_key = self.required_key

        if isclass(controller_or_action) and \
                issubclass(controller_or_action, WebMonitorController):
            actions = get_controller_actions(controller_or_action.__dict__)
            for action in actions.values():
                self(action)
        else:
            if not hasattr(controller_or_action, allow_key) and\
                    hasattr(self, 'allow'):
                setattr(controller_or_action, allow_key, self.allow)
            if not hasattr(controller_or_action, deny_key) and\
                    hasattr(self, 'deny'):
                setattr(controller_or_action, deny_key, self.deny)
            if not hasattr(controller_or_action, required_key) and\
                    hasattr(self, 'required'):
                setattr(controller_or_action, required_key, self.required)
        return controller_or_action
