import urllib

_CONTROLLER_MISSING_ERROR = \
        'controller argument is necessary when initialized without a default'
_ACTION_MISSING_ERROR = \
        'action argument is necessary when initialized without a default'



class UrlHelper(object):

    def __init__(self, app_directory='', action_name=None, controller_name=None):
        self.app_directory = app_directory
        self.controller_name = controller_name
        self.action_name = action_name

    def static(self, path):
        if path.startswith('/'):
            # Absolute path, strip the '/' since we are appending it
            path = path[1:]
        return '%s/%s' % (self.app_directory, path)

    def action(self, name=None, controller=None, **parameters):
        if not controller:
            if not self.controller_name:
                raise ValueError(_CONTROLLER_MISSING_ERROR)
            controller = self.controller_name
        if not name:
            if not self.action_name:
                raise ValueError(_ACTION_MISSING_ERROR)
            name = self.action_name

        qs = ''
        if parameters:
            qs = urllib.urlencode(parameters)
            qs = '?' + qs
            
        return '%s/%s/%s%s' % (self.app_directory, controller, name, qs)


class HtmlHelper(object):
    pass
