

class Context(object):
    """
    Represents a request-specific context.

    This is used to store request-specific data, such as database
    connections/transactions or anything else that should live in a single
    HTTP Request.
    """
    pass
