import logging
from datetime import timedelta, datetime
from traceback import format_exc
from daemons.webpage import DAEMON as webpage_daemon
from task import Task
from services.webpage import WebpageService
from datetime import datetime


__logger = logging.getLogger('models.task.update_resource')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


webpage_service = WebpageService(None)


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
