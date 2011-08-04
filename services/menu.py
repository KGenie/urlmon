from app_components.service import Service
from helpers import UrlHelper
from config import CONTROLLER_CACHE
from threading import Lock
from util import is_authorized, get_controller_actions
from sets import ImmutableSet

_u = UrlHelper()
_cache_lock = Lock()
_menu_cache = {}


class MenuItem(object):

    def __init__(self, label, controller, action):
        self.label = label
        self.controller = controller
        self.action = action
        
    @property
    def url(self):
        return _u.action(self.action, self.controller)

    def __repr__(self):
        return self.label

class Menu(object):

    def __init__(self, label, children):
        self.label = label
        self.children = children

    def __repr__(self):
        return self.label


def menu(label=None, exclude=False):
    def dec(fn):
        if not exclude:
            lbl = label
            if not lbl:
                lbl = fn.__name__
            setattr(fn, '_menu_label', lbl)
        setattr(fn, '_menu_decorated', True)
        return fn
    return dec

menu_decorator_instance = menu()

class MenuService(Service):

    def sitemap(self):
        user = self.context.environ.get('user', None)
        roles = None
        if not user:
            roles = []
        else:
            roles = user.roles
        return self.get_sitemap(roles)


    def get_sitemap(self, roles):
        """
        Calculates and returns the site menu.

        This will compute the site menu for the user with permissions described
        in 'roles'. For each combination
        """
        s = ImmutableSet(roles)
        if s not in _menu_cache:
            _cache_lock.acquire()
            if s not in _menu_cache:
                sitemap = []
                for controller, controller_class in CONTROLLER_CACHE.items():
                    actions = []

                    if not hasattr(controller_class, '_menu_decorated'):
                        menu_decorator_instance(controller_class)

                    # get the possible controller actions(which support GET)
                    acts = ((n,a) for n,a in
                            controller_class._actions.items() if
                                    hasattr(a, '_methods_allowed') and
                                    'GET' in a._methods_allowed)

                    # decorates those that have not been decorated yet
                    acts2 = []
                    for name, action in acts:
                        if not hasattr(action, '_menu_decorated'):
                            menu_decorator_instance(action)
                        if hasattr(action, '_menu_label'):
                            acts2.append((name,action))
    
                    # iterates for the last time, filtering those that don't
                    # have label
                    for name, action in acts2:
                        if not action._authentication_required or\
                            is_authorized(roles, action._roles_allowed,
                                action._roles_denied):
                            actions.append(MenuItem(action._menu_label, controller, action))

                    if actions:
                        sitemap.append(Menu(controller_class._menu_label, actions))
                _menu_cache[s] = sitemap
            _cache_lock.release()
        return _menu_cache[s]

