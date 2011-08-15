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
        debug('Starting task scheduler')
        sleep(1)
        pool = ThreadPool(self.threads)
        while 1:
            time = datetime.now()
            debug('Began to run tasks at %s' % time)
            try:
                service = TaskService(None)
                tasks = service.get_all()
            except Exception, e:
                error('An error ocurred while retrieving all tasks: %s' %
                        format_exc(e))
            else:
                debug('Tasks retrieved: %s. preparing to run all' % tasks)
                try:
                    for task in tasks:
                        if task.match(time):
                            pool.apply_async(self.run_task, args=(task,))
                except Exception, e:
                    error('An error ocurred while executing one or more tasks: %s '
                            % format_exc(e))

            # check for scheduled tasks again in at most one minute
            time += timedelta(seconds=5)
            current = datetime.now()
            while current < time:
                current = datetime.now()
                if current > time:
                    current = time
                sleeptime = max((time - current).seconds, 0)
                sleep(sleeptime)


    def run_task(self, task):
        debug('Running task %s' % task.id)


    def enqueue_task(self, task):
        runner = self.runqueue.get()
        runner.run_task(task)
        self.runqueue.put(runner)


DAEMON = TaskDaemon()
