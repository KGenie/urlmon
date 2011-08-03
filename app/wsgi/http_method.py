from app_components.response import MethodNotAllowedResponse

class HTTPMethodMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        action_callable = environ['route']['action_callable']

        if method not in action_callable._methods_allowed:
            return MethodNotAllowedResponse()
        return self.app(environ, start_response)


def __method_decorator(func):
    if not hasattr(func, '_methods_allowed'):
        setattr(func, '_methods_allowed', set())

def post(func):
    __method_decorator(func)
    func._methods_allowed.add('POST')
    return func
    
def get(func):
    __method_decorator(func)
    func._methods_allowed.add('GET')
    return func
