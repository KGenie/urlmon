import logging
from datetime import timedelta, datetime
from traceback import format_exc
from app_components.model import Model
from daemons.webpage import DAEMON as webpage_daemon
from daemons.mailer import DAEMON as mailer_daemon
from services.webpage import WebpageService
from services.tracker import TrackerService
from services.user import UserService
from datetime import datetime
from lxml import etree, html
from hashlib import sha1
from string import Template

_new_template = Template(u"""You have successfully began to track content!

The page is located at $url

Here is the content you are tracking:

"$new_content"

We will continue to track changes on that page for you!
""")
_updated_template = Template(u"""One of your watched web pages has changed!

The page is located at $url

Here is the status:

"$old_content" 

Changed to

"$new_content"

We will continue to track changes on that page for you!
""")

__logger = logging.getLogger('models.task')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


webpage_service = WebpageService(None)
tracker_service = TrackerService(None)
user_service = UserService(None)


class Task(Model):

    def __init__(self, id=None, next_run=None):
        self.id = id
        self.next_run = next_run


    def run(self):
        debug('Running task %s' % self.id)
        self.run_override()


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
        debug('Sending notification to user')
        user = user_service.get(tracker.user_id)

        if self.last_content:
            msg = _updated_template.substitute(
                    new_content=changes[0], old_content=self.last_content,
                    url=tracker.url)
        else:
            msg = _new_template.substitute(
                    new_content=changes[0], url=tracker.url)


        self.last_content = changes[0]
        subject = 'The page at %s has changed' % tracker.url
        mailer_daemon.sendmail(user.email, subject, msg)
        debug('Notification successfully sent')



class UpdateResource(Task):

    def __init__(self, url, *args, **kwargs):
        Task.__init__(self, *args, **kwargs)
        self.url = url


    def run_override(self):
        debug('Downloading web page at %s...', self.url)
        new_page = webpage_daemon.fetch(self.url)
        debug('Web page downloaded. Retrieving the stored version...')
        stored_page = webpage_service.get_by_url(self.url)

        if stored_page != None and stored_page.digest != new_page.digest:
            debug('Old digest %s, new digest %s' % (stored_page.digest,\
                new_page.digest))
            debug('Stored version is outdated, updating it now')
            now = datetime.now()
            new_page.last_modified = now
            webpage_service.update(stored_page.id, new_page)
            debug('Web page at %s was updated' % self.url)
        elif stored_page == None:
            debug('This is the first time we are downloading this page')
            now = datetime.now()
            new_page.last_modified = now
            webpage_service.insert(new_page)
            debug('Web page successfully stored')
        else:
            debug('Stored version is up to date')
        self.next_run = datetime.now() + timedelta(seconds=60) 
