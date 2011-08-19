import inspect

def _declare_services(cls, name, bases, attrs):
    services = dict((k,v) for k,v in attrs.items()\
                if inspect.isclass(v) and\
                issubclass(v, basestring))

    attrs['_services'] = services
    for k, v in services.items():
        attrs[k] = None



class ServiceMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name != 'Service':
            _declare_services(cls, name, bases, attrs)
        return super(ServiceMetaclass, cls).__new__(cls, name, bases, attrs)


class Service(object):
    """
    Generic service representation.

    This class represents a service. Each service has a context-specific
    life cycle.
    """
    __metaclass__ = ServiceMetaclass


    def __init__(self, context):
        self.context = context
