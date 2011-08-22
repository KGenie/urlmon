import logging
from daemons.daemon import Daemon
from traceback import format_exc
from datetime import datetime, timedelta
from time import sleep
from models.task import Task
from app_config import INTERVAL_BETWEEN_TASK_CHECKS
from database.sqlalch import Session


__logger = logging.getLogger('daemons.cleanup')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


class CleanupDaemon(Daemon):

    def __init__(self, stdin='/dev/null', stdout='/dev/null', 
            stderr='/dev/null'):
        Daemon.__init__(self, stdin, stdout, stderr)
        

    def run(self):
        debug('Starting cleanup daemon')
        sleep(2)

        while 1:
            max_idle_interval = \
                    timedelta(seconds=INTERVAL_BETWEEN_TASK_CHECKS)
            debug('Looking for tasks that were running for a long time')
            try:
                session = Session()
                now = datetime.now()
                tasks = session.query(Task).\
                        filter(Task.is_running == True).\
                        filter(Task.next_run <= \
                        (now - max_idle_interval)).all()
            except Exception, e:
                error('An error ocurred while retrieving tasks: %s' %
                        format_exc(e))
            else:
                try:
                    if tasks:
                        warn('Found tasks there were running for more than %s seconds! Cleaning up...' % max_idle_interval.seconds)
                                
                        for task in tasks:
                            task.is_running = False
                except Exception, e:
                    session.rollback()
                    error('An error ocurred while cleaning one or more tasks: %s ' % format_exc(e))
                else:
                    session.commit()
                    session.close()
            sleep(INTERVAL_BETWEEN_TASK_CHECKS)

DAEMON = CleanupDaemon()
