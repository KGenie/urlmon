from task import Task


class UpdateResource(Task):

    def __init__(self, url, *args, **kwargs):
        Task.__init__(self, *args, **kwargs)
        self.url = url
