import inspect
from app_components.service import Service

def is_authorized(user_roles, authorized_roles, denied_roles):
    """
    Returns True if the user with roles specified in 'user_roles' is 
    authorized, taking into consideration 'authorized_roles' and 'denied_roles'
    """
    if '*' in denied_roles:
        return False
    if '*' in authorized_roles:
        authorized_roles = user_roles

    
    user_roles = set(user_roles)
    authorized_roles = set(authorized_roles)
    denied_roles = set(denied_roles)
    return bool(user_roles.difference(denied_roles)) and\
            bool(user_roles.intersection(authorized_roles))



def get_controller_actions(controller_dict):
    return dict((k,v) for k,v in controller_dict.items() \
                if hasattr(v, '_methods_allowed'))

def get_controller_services(controller_dict):
    return dict((k,v) for k,v in controller_dict.items() \
                if inspect.isclass(v) and\
                issubclass(v, Service))


def get_controller_class_name(module_name):
    """
    Gets the controller class name from the module name.

    Dashes are replaced with underscore.
    This was copied from the pylons framework.
    """
    words = module_name.replace('-', '_').split('_')
    return ''.join(w.title() for w in words) + 'Controller'
