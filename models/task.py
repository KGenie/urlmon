import logging
from app_components.model import Model


class Task(Model):

    def __init__(self, next_run=None):
        self.next_run = next_run
        self.is_running = False

