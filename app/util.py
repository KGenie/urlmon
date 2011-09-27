import inspect
from app_components.service import Service
from urlparse import urlparse, urlunparse

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
            not user_roles.isdisjoint(authorized_roles)


def normalize_url(url):
    if '//' not in url:
        url = '//' + url
    u = list(urlparse(url))
    if u[0] == '':
        u[0] = 'http'
    u = urlunparse(u)
    return u


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


def get_page_range(total_pages, current_page, range_size):
    range_size = range_size 
    offset = range_size // 2
    min_page = current_page - offset
    max_page = current_page + offset
    # so far we handle the 'good' case, where the 'range_size' is odd,
    # 'current page' "sits" in the middle of the sequence delimited
    # by 'min_page' and 'max_page',  'min_page' >= 1 and 'max_page' <=
    # 'total_pages'


    if min_page < 1:
        # This means that the we should 'move' the sequence up, until its
        # min value is 1.
        max_delta = 1 - min_page 
        max_page = max_page + max_delta 
        min_page = 1
        if max_page > total_pages:
            # if by moving up we breached the 'total_pages' limit, just
            # bring it back
            max_page = total_pages
    if max_page > total_pages:
        min_delta = max_page - total_pages
        min_page = min_page - min_delta
        max_page = total_pages
        if min_page < 1:
            min_page = 1
        

    result = range(min_page, max_page + 1)
    if len(result)> range_size:
         return result[1:]
    return result


