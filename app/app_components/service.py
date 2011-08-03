
class ServiceMetaclass(type):

    def __new__(cls, name, bases, attrs):

        return super(ServiceMetaclass).__new__(cls, name, bases, attrs)



class Service(object):
    """
    Generic service representation.

    This class represents a service. Each service has a context-specific
    life cycle.
    """


    def __init__(self, context):
        self.context = context
