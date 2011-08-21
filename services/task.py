from datetime import datetime, timedelta
from storage import StorageService
from models.task import Task

class TaskService(StorageService):
    entity = Task

