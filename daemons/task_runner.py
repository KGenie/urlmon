from datetime import datetime, timedelta
from time import sleep
from tasks.task_runner import TaskRunner
from services.scheduled_task import TaskService
from Queue import Queue


def daemonize():
    scheduler = TaskScheduler()



class TaskScheduler(object):

    def __init__(self, runners=1, threads_per_runner=5):
        self.runners = runners
        self.runqueue = Queue()
        for i in range(runners):
            self.runqueue.put(TaskRunner(thread_count=threads_per_runner))


    def run(self):
        time = datetime.now()
        while 1:
            service = TaskService(None)
            tasks = service.get_all()
            for task in tasks:
                if task.match(time):
                    self.enqueue_task(task)

            # check for scheduled tasks again in at most one minute
            time += timedelta(minutes=1)
            while datetime.now() < time:
                sleep((time - datetime.now()).seconds)


    def enqueue_task(self, task):
        runner = self.runqueue.get()
        runner.run_task(task)
        self.runqueue.put(runner)
