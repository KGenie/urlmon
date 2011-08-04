"""
WSGI Middleware responsible for resolving controllers

This implements the basic controller dispatching mechanism based on Pylons 
framework.
"""
import sys
from app_components.response import NotFoundResponse

class ControllerMiddleware(object):
    """
    Middleware responsible for setting up the controller class.

    This middleware should contain all the logic regarding resolving
    controller classes
    """

    def __init__(self, app, controller_cache):
        """
        Middleware initializer.

        Setup the controller class cache, and the lock for modifying it,
        since multiple threads accessing/modifying it can result in a 
        race condition.
        """
        self.app = app
        self.controller_cache = controller_cache


    def get_controller_class(self, environ):
        """
        Gets controller class that will handle the request.
        """
        controller_name = environ['route']['controller']
        controller_class = self.controller_cache.get(controller_name, None)
        return controller_class


    def set_route_variables(self, environ):
        match = environ['wsgiorg.routing_args'][1]
        route = {
                'controller': match.get('controller', None),
                'action': match.get('action', None),
                'id': match.get('id', None)
                }
        environ['route'] = route


    def get_action_callable(self, environ, controller_class):
        if not controller_class:
            return None

        action_name = environ['route']['action']

        if not action_name or action_name not in controller_class._actions:
            return None

        return controller_class._actions[action_name]


    def __call__(self, environ, start_response):
        self.set_route_variables(environ)
        controller_class = self.get_controller_class(environ)
        action_callable = self.get_action_callable(environ, controller_class)

        if not action_callable:
            return NotFoundResponse()
        else:
            environ['route']['controller_class'] = controller_class
            environ['route']['action_callable'] = action_callable
            return self.app(environ, start_response)
