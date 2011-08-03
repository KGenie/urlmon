from app_components.request import Request

class RequestMiddleware(object):
    """
    Middleware for creation of 'Request' objects.

    This will create a Request object and inject it into the
    WSGI environment.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        environ['request'] = request
        return self.app(environ, start_response)
