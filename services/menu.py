from app_components.service import Service
from helpers import UrlHelper
from config import CONTROLLER_CACHE
from threading import Lock
from util import is_authorized, get_controller_actions
from sets import ImmutableSet
from helpers import menu

_u = UrlHelper()
_cache_lock = Lock()
_menu_cache = {}

def menu_order(key):
    key = key.controller.lower()
    if 'home' == key:
        return 0
    elif 'tracker' == key:
        return 1
    elif 'tracker_group' == key:
        return 2
    elif 'user' == key:
        return 3
    else:
        return 9999


class MenuItem(object):

    def __init__(self, label=None, controller=None, action=None):
        self.label = label
        self.controller = controller
        self.action = action
        
    @property
    def url(self):
        return _u.action(self.action, self.controller)

    def __repr__(self):
        return self.label

class Menu(MenuItem):

    def __init__(self, label, children):
        item = children[0]
        self.controller = item.controller
        self.action = item.action
        if len(children) == 1:
            self.label = item.label
            self.children = None
        else:
            self.label = label
            self.children = children


menu_decorator_instance = menu()

class MenuService(Service):

    def sitemap(self):
        user = self.context.environ['beaker.session'].get('user', None)
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
                            actions.append(MenuItem(label=action._menu_label,
                                controller=controller, action=action.__name__))

                    if actions:
                        sitemap.append(Menu(label=controller_class._menu_label,
                            children=actions))
                _menu_cache[s] = sorted(sitemap, key=menu_order)
            _cache_lock.release()
        return _menu_cache[s]

