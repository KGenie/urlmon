import logging
from sqlalchemy import desc
from traceback import format_exc
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool
from time import sleep
from models.task import Task
from models.update_resource import UpdateResource
from models.user import User
from models.webpage import Webpage
from models.webpage_version import WebpageVersion
from models.tracker_change import TrackerChange
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

    now = datetime.now()
   
    webpage = tracker.webpage

    time_since_last_checked = now - webpage.last_checked
    # Checking if the page should be updated
    if time_since_last_checked.total_seconds() >= tracker.frequency +\
            INTERVAL_BETWEEN_TASK_CHECKS:

        ur_task = session.query(UpdateResource).filter(\
            UpdateResource.url == tracker.url).first()

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


    stored_version = get_last_page_version(tracker.url)

    selector = tracker.css_selector
    dom = html.fromstring(stored_version.content, base_url=tracker.url)
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

    last_tracker_change = get_last_tracker_change(tracker.id)
    old_digest = None
    old_content = None
    if last_tracker_change:
        old_digest = last_tracker_change.digest
        old_content = last_tracker_change.content
    # Here we need to query the tracker_changes table for the last change
    if digest != old_digest:
        # TODO now we should store a new record in the tracker_changes table
        # and send an email to the user
        debug('Tracked content at %s was updated' % tracker.url)
        change = TrackerChange(tracker.id, stored_version.id, updated_content)
        send_mail(task, updated_content, old_content)
        session.add(change)
    else:
        debug('There wasnt any relevant modification to %s' % tracker.url)

    task.next_run = datetime.now() + timedelta(seconds=tracker.frequency)
    debug('Next run is scheduled for %s' % task.next_run)


def get_last_tracker_change(tracker_id):
    session = Session()
    return session.query(TrackerChange)\
            .filter(TrackerChange.tracker_id == tracker_id)\
            .order_by(desc(TrackerChange.id))\
            .first()


def get_last_page_version(url):
    session = Session()
    return session.query(WebpageVersion)\
            .filter(WebpageVersion._url == url)\
            .order_by(desc(WebpageVersion.id))\
            .first()


def run_update_resource(task):
    session = Session()
    now = datetime.now()
    debug('Downloading web page at %s...', task.url)
    new_version = webpage_daemon.fetch(task.url)
    debug('Web page downloaded. Retrieving the stored version...')

    task.webpage.last_checked = now

    stored_version = get_last_page_version(task.url)

    if new_version != None:
        add = False
        if stored_version != None:
            if stored_version.digest != new_version.digest:
                debug('Last version of %s is outdated, adding a new version'\
                        % task.url)
                add = True
        else:
            debug('This is the first time we are downloading %s' % task.url)
            add = True
        if add:
            session.add(new_version)
            debug('New version of %s successfully stored' % task.url)
        else:
            debug('Stored version of %s was up to date' % task.url)
    else:
        error('There was an error when retrieving %s. Exiting' % task.url)

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
