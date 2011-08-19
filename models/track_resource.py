import logging
from datetime import timedelta, datetime
from traceback import format_exc
from daemons.mailer import DAEMON as mailer_daemon
from services import webpage as webpage_service_module
from services import tracker as tracker_service_module
from services import user as user_service_module
from datetime import datetime
from lxml import etree, html
from hashlib import sha1
from task import Task

__logger = logging.getLogger('models.task.track_resource')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info



class TrackResource(Task):

    def __init__(self, tracker_id, last_content='', *args, **kwargs):
        Task.__init__(self, *args, **kwargs)
        self.tracker_id = tracker_id
        self.last_content = last_content

    @property
    def last_content(self):
        return self._last_content


    @last_content.setter
    def last_content(self, value):
        h = sha1()
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        h.update(value)
        self.last_digest = h.hexdigest()        
        self._last_content = value


    def run_override(self):
        webpage_service = webpage_service_module.WebpageService(None)
        tracker_service = tracker_service_module.TrackerService(None)

        debug('Preparing check url for changes')
        tracker = tracker_service.get(self.tracker_id)
        if tracker != None:
            debug('Tracker successfully retrieved')
        else:
            error('Tracker not found, skipping task with id: %s' % self.id)
            return
        stored_page = webpage_service.get_by_url(tracker.url)
        if stored_page == None:
            error('Page was not previously stored, skipping task with id: %s' % 
                    self.id)
            return
        selector = tracker.css_selector
        dom = html.fromstring(stored_page.contents, base_url=tracker.url)
        debug('Stored page successfully retrieved and parsed')
        h = sha1()
        new_elements = []
        for watched in dom.cssselect(selector):
            watched_contents = etree.tostring(watched, encoding=unicode, method='text')
            new_elements.append(watched_contents)
            h.update(watched_contents.encode('utf-8'))
        digest = h.hexdigest()
        if digest != self.last_digest:
            debug('Page at %s was updated' % tracker.url)
            self.last_digest = digest
            self.send_mail(tracker, new_elements)
        else:
            debug('There wasnt any relevant modification to %s' % tracker.url)

        self.next_run = datetime.now() + tracker.frequency
        debug('Next run is scheduled for %s' % self.next_run)

    

    def send_mail(self, tracker, changes):
        user_service = user_service_module.UserService(None)
        debug('Sending notification to user')
        user = user_service.get(tracker.user_id)
        debug('CHANGES %s' % changes[0].__class__)

        if self.last_content:
            subject = 'The page at %s has changed' % tracker.url
            template_name = 'tracker_updated'
            template_context = { 'url': tracker.url, 'new_content': changes[0],
                    'old_content': self.last_content }
        else:
            subject = 'Tracking %s' % tracker.url
            template_name = 'tracker_started'
            template_context = { 'url': tracker.url, 'new_content': changes[0] }


        self.last_content = changes[0]
        mailer_daemon.send_template_mail(user.email, subject, template_name,
                template_context)
        debug('Notification successfully sent')
