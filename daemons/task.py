import logging
from traceback import format_exc
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
from services.task import TaskService
from daemons.daemon import Daemon


__logger = logging.getLogger('daemons.task')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info

class TaskDaemon(Daemon):

    def __init__(self, threads=5, stdin='/dev/null', stdout='/dev/null', 
            stderr='/dev/null'):
        Daemon.__init__(self, stdin, stdout, stderr)
        self.threads = threads
        

    def run(self):
        try:
            debug('Starting task scheduler')
            time = datetime.now()
            sleep(2)
            pool = ThreadPool(self.threads)
        except Exception, ex:
            error('An error ocurred while beginning task scheduler: %s' %
                        format_exc(ex))

        while 1:
            debug('Began to run tasks at %s' % time)
            try:
                service = TaskService(None)
                tasks = service.get_tasks_to_run()
            except Exception, e:
                error('An error ocurred while retrieving all tasks: %s' %
                        format_exc(e))
            else:
                debug('Tasks retrieved: %s. preparing to run all' % tasks)
                try:
                    for task in tasks:
                        pool.apply_async(self.run_task, args=(task, service))
                except Exception, e:
                    error('An error ocurred while dispatching one or more tasks: %s '
                            % format_exc(e))
            sleep(5)


    def run_task(self, task, task_service):
        try:
            task.run()
            task_service.update(task.id, task)
        except Exception, e:
            error('An error occurred while executing a task: %s' %
                    format_exc(e))


    def enqueue_task(self, task):
        runner = self.runqueue.get()
        runner.run_task(task)
        self.runqueue.put(runner)


DAEMON = TaskDaemon()
