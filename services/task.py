from storage import StorageService
from models.task import Task


class TaskService(StorageService):

    @classmethod
    def stub_data(cls):
        cls.insert(Task(type=1))

