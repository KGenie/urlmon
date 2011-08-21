from datetime import datetime, timedelta
from storage import StorageService
from models.task import Task

class TaskService(StorageService):
    entity = Task

    def get_tasks_to_run(self):
        now = datetime.now()
        return self.session.query(Task).\
                filter(Task.next_run <= now)
