from app_components.response import JinjaResponse, RedirectResponse
from meta import WebMonitorControllerMetaclass

class WebMonitorController(object):
    __metaclass__ = WebMonitorControllerMetaclass

           
    def __call__(self, environ, start_response):
        """
        Invokes the controller to obtain a response.
        
        This will invoke the requested action already present in the
        WSGI environment.
        """
        action = environ['route']['action_callable']
        return action(self, self.request)


    def view(self, model=None, name=None):
        view_name_format = '%s.htmljinja'
        if not name:
            name = self.request.environ['route']['action']
        controller_name = self.request.environ['route']['controller']
        name = view_name_format % name
        return JinjaResponse(self.request, name, controller_name,\
                model)

    def redirect(self, action, controller=None, **qsargs):
        if not controller:
            controller = self.request.environ['route']['controller']

        return RedirectResponse(controller=controller, action=action,
                qsargs=qsargs)
