import logging
from traceback import format_exc
from app_components.model import Model


__logger = logging.getLogger('models.task')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


class Task(Model):

    def __init__(self, id=None, next_run=None):
        self.id = id
        self.next_run = next_run


    def run(self):
        debug('Running task %s' % self.id)
        self.run_override()
