"""
Main Url Monitor app module

This module contains the WSGI application class
"""
   


class WebMonitorApp(object):
    """
    Web Monitor WSGI application.

    An instance of this class Implements the WSGI application object as
    specified in PEP 333.
    This class will simply retrieve a controller instance - which is just 
    another WSGI app - and invoke it.
    """

    def __call__(self, environ, start_response):
        controller = environ['route']['controller_instance']
        return controller(environ, start_response)
