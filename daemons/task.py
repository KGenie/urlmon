import logging
from traceback import format_exc
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool
from time import sleep
from models.task import Task
from models.update_resource import UpdateResource
from models.user import User
from models.webpage import Webpage
from daemons.daemon import Daemon
from daemons.mailer import DAEMON as mailer_daemon
from daemons.webpage import DAEMON as webpage_daemon
from app_config import NUMBER_OF_TASK_RUNNERS, \
        INTERVAL_BETWEEN_TASK_CHECKS
from lxml import etree, html
from database.sqlalch import Session
from hashlib import sha1


__logger = logging.getLogger('daemons.task')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


class TaskDaemon(Daemon):

    def __init__(self, stdin='/dev/null', stdout='/dev/null', 
            stderr='/dev/null'):
        Daemon.__init__(self, stdin, stdout, stderr)
        self.threads = NUMBER_OF_TASK_RUNNERS
        

    def run(self):
        try:
            debug('Starting task scheduler')
            sleep(2)
            pool = Pool(self.threads)
        except Exception, ex:
            error('An error ocurred while beginning task scheduler: %s' %
                        format_exc(ex))

        while 1:
            debug('Looking for tasks to run')
            try:
                now = datetime.now()
                task_ids = Session().query(Task.id).\
                        filter(Task.next_run <= now).\
                        filter(Task.is_running == False)
            except Exception, e:
                error('An error ocurred while retrieving all tasks: %s' %
                        format_exc(e))
            else:
                try:
                    for task_id in task_ids:
                        pool.apply_async(self.run_task, args=(task_id))
                except Exception, e:
                    error('An error ocurred while dispatching one or more tasks: %s '
                            % format_exc(e))
            sleep(INTERVAL_BETWEEN_TASK_CHECKS)


    def run_task(self, task_id):
        try:
            debug('Running task with id %s' % task_id)
            session = Session()
            task = session.query(Task).get(task_id)
            task.is_running = True
            session.commit()
            
            task_type = task.type
            if task_type == 1:
                run_track_resource(task)
            elif task_type == 2:
                run_update_resource(task)
            task.is_running = False
            session.commit()
        except Exception, e:
            session.rollback()
            task.is_running = False
            session.commit()
            error('An error occurred while executing a task: %s' %
                    format_exc(e))


    def enqueue_task(self, task):
        runner = self.runqueue.get()
        runner.run_task(task)
        self.runqueue.put(runner)


DAEMON = TaskDaemon()


def run_track_resource(task):
    session = Session()
    debug('Preparing check url for changes')
    tracker = task.tracker
    if not tracker:
        warn('Tracker not found, skipping task')
        return

    stored_page = tracker.webpage

    now = datetime.now()

    ur_task = session.query(UpdateResource).filter(\
            UpdateResource.url == tracker.url).first()

    update = False
    if stored_page:
        time_since_last_updated = now - stored_page.last_updated
        if time_since_last_updated.total_seconds() >= tracker.frequency +\
                INTERVAL_BETWEEN_TASK_CHECKS:
            update = True
    else:
        update = True

    if update:
        if not ur_task:
            ur_task = UpdateResource(url=tracker.url)
            session.add(ur_task)

        warn('Page at %s must be updated' % tracker.url)
        if not ur_task.is_running:
            warn('Scheduling an update for the next run cycle')
            ur_task.next_run = now
        else:
            warn('URL is currently being downloaded.')
        warn('Will try to run this task again soon')
        return


    selector = tracker.css_selector
    dom = html.fromstring(stored_page.contents, base_url=tracker.url)
    debug('Stored page successfully retrieved and parsed')
    h = sha1()
    selected = list(dom.cssselect(selector))
    if not selected:
        warn('We didn''t find anything using the previous selector!')
        warn('Changing the selector to ''body'' and sending notification to warn the user!')
        tracker.css_selector = 'body'
        send_warning_mail(task)
        return
    else:
        updated_content = etree.tostring(selected[0],\
                encoding=unicode, method='text')
        h.update(updated_content.encode('utf-8'))
    digest = h.digest()
    if digest != task.last_digest:
        debug('Page at %s was updated' % tracker.url)
        old_content = task.last_content
        task.last_content = updated_content
        send_mail(task, updated_content, old_content)
    else:
        debug('There wasnt any relevant modification to %s' % tracker.url)

    task.next_run = datetime.now() + timedelta(seconds=tracker.frequency)
    debug('Next run is scheduled for %s' % task.next_run)



def run_update_resource(task):
    session = Session()
    now = datetime.now()
    debug('Downloading web page at %s...', task.url)
    new_page = webpage_daemon.fetch(task.url)
    debug('Web page downloaded. Retrieving the stored version...')
    stored_page = task.webpage

    if stored_page:
        stored_page.last_updated = now

    if stored_page != None and new_page != None and\
            stored_page.digest != new_page.digest:
        debug('Stored version is outdated, updating it now')
        now = datetime.now()
        stored_page.contents = new_page.contents
        debug('Web page at %s was updated' % task.url)
    elif stored_page == None:
        debug('This is the first time we are downloading this page')
        now = datetime.now()
        new_page.last_updated = now
        session.add(new_page)
        debug('Web page successfully stored')
    elif new_page == None:
        error('There was an error when retrieving %s. Exiting.' % task.url)
    else:
        debug('Stored version is up to date')
    session.delete(task)


def send_warning_mail(task):
    tracker = task.tracker
    tracker_group = tracker.tracker_group
    user = tracker_group.user
    debug('Sending warning to %s' % user.email)

    subject = 'Warning: The page at %s has changed, but its tracker must be updated.' % tracker.url
    template_name = 'tracker_not_found'
    template_context = { 'url': tracker.url }

    mailer_daemon.send_template_mail(user.email, subject, template_name,
            template_context)
    debug('Warning successfully sent')


def send_mail(task, updated_content, old_content):
    tracker = task.tracker
    tracker_group = tracker.tracker_group
    user = tracker_group.user
    debug('Sending notification to %s' % user.email)

    if old_content:
        subject = 'The page at %s has changed' % tracker.url
        template_name = 'tracker_updated'
        template_context = { 'url': tracker.url, 'new_content': updated_content,
                'old_content': old_content }
    else:
        subject = 'Tracking %s' % tracker.url
        template_name = 'tracker_started'
        template_context = { 'url': tracker.url, 'new_content': updated_content }


    mailer_daemon.send_template_mail(user.email, subject, template_name,
            template_context)
    debug('Notification successfully sent')
