import logging
from traceback import format_exc
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
from services.task import TaskService
from daemons.daemon import Daemon
from daemons.mailer import DAEMON as mailer_daemon
from daemons.webpage import DAEMON as webpage_daemon
from services.tracker import TrackerService
from services.user import UserService
from services.webpage import WebpageService
from lxml import etree, html


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
            name = task.__class__.__name__
            if name == 'TrackResource':
                run_track_resource(task)
            elif name == 'UpdateResource':
                run_update_resource(task)
            task_service.update(task.id, task)
        except Exception, e:
            error('An error occurred while executing a task: %s' %
                    format_exc(e))


    def enqueue_task(self, task):
        runner = self.runqueue.get()
        runner.run_task(task)
        self.runqueue.put(runner)


DAEMON = TaskDaemon()


def run_track_resource(task):
    webpage_service = WebpageService(None)
    tracker_service = TrackerService(None)

    debug('Preparing check url for changes')
    tracker = tracker_service.get(task.tracker_id)
    if tracker != None:
        debug('Tracker successfully retrieved')
    else:
        error('Tracker not found, skipping task with id: %s' % task.id)
        return
    stored_page = webpage_service.get_by_url(tracker.url)
    if stored_page == None:
        error('Page was not previously stored, skipping task with id: %s'\
                % task.id)
        return
    selector = tracker.css_selector
    dom = html.fromstring(stored_page.contents, base_url=tracker.url)
    debug('Stored page successfully retrieved and parsed')
    h = sha1()
    new_elements = []
    for watched in dom.cssselect(selector):
        watched_contents = etree.tostring(watched,\
                encoding=unicode, method='text')
        new_elements.append(watched_contents)
        h.update(watched_contents.encode('utf-8'))
    digest = h.hexdigest()
    if digest != task.last_digest:
        debug('Page at %s was updated' % tracker.url)
        task.last_digest = digest
        task.send_mail(tracker, new_elements)
    else:
        debug('There wasnt any relevant modification to %s' % tracker.url)

    task.next_run = datetime.now() + tracker.frequency
    debug('Next run is scheduled for %s' % task.next_run)



def run_update_resource(task):
    debug('Downloading web page at %s...', task.url)
    new_page = webpage_daemon.fetch(task.url)
    debug('Web page downloaded. Retrieving the stored version...')
    stored_page = webpage_service.get_by_url(task.url)

    if stored_page != None and stored_page.digest != new_page.digest:
        debug('Old digest %s, new digest %s' % (stored_page.digest,\
            new_page.digest))
        debug('Stored version is outdated, updating it now')
        now = datetime.now()
        new_page.last_modified = now
        webpage_service.update(stored_page.id, new_page)
        debug('Web page at %s was updated' % task.url)
    elif stored_page == None:
        debug('This is the first time we are downloading this page')
        now = datetime.now()
        new_page.last_modified = now
        webpage_service.insert(new_page)
        debug('Web page successfully stored')
    else:
        debug('Stored version is up to date')
    task.next_run = datetime.now() + timedelta(seconds=60) 



def send_mail(task, tracker, changes):
    user_service = UserService(None)
    debug('Sending notification to user')
    user = user_service.get(tracker.user_id)
    debug('CHANGES %s' % changes[0].__class__)

    if task.last_content:
        subject = 'The page at %s has changed' % tracker.url
        template_name = 'tracker_updated'
        template_context = { 'url': tracker.url, 'new_content': changes[0],
                'old_content': task.last_content }
    else:
        subject = 'Tracking %s' % tracker.url
        template_name = 'tracker_started'
        template_context = { 'url': tracker.url, 'new_content': changes[0] }


    task.last_content = changes[0]
    mailer_daemon.send_template_mail(user.email, subject, template_name,
            template_context)
    debug('Notification successfully sent')
