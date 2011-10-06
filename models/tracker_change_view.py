from hashlib import sha1
from app_components.model import Model

class TrackerChangeView(Model):

    MAX_CONTENT_LENGTH = 250
    MAX_URL_LENGTH = 50

    def __init__(self, tracker_change, now):
        self.id = tracker_change.id
        self.tracker_id = tracker_change.tracker.id
        self.tracker_url = tracker_change.tracker.webpage.url
        self.tracker_name = tracker_change.tracker.name
        self.content = tracker_change.content
        self.date = tracker_change.webpage_version.date
        self.now = now
        self.start_index = tracker_change.start_index



    @property
    def time_ago(self):
        diff = self.now - self.date
        if diff.days == 1:
            return '1 day ago'
        elif diff.days > 1:
            return '%s days ago' % diff.days
        elif diff.seconds >= 7200:
            return '%s hours ago' % (diff.seconds / 3600)
        elif diff.seconds >= 3600:
            return '1 hour ago'
        elif diff.seconds >= 120:
            return '%s minutes ago' % (diff.seconds / 60)
        else:
            return '1 minute ago'



    @property
    def tracker_url_short(self):
        if len(self.tracker_url) > self.MAX_URL_LENGTH:
            return self.tracker_url[:self.MAX_URL_LENGTH] + ' ...'
        return self.tracker_url
        

    @property
    def content_short(self):
        s = self.content[self.start_index:]
        if len(s) > self.MAX_CONTENT_LENGTH:
            ret = s[:self.MAX_CONTENT_LENGTH] + ' ...'
            return ret
        return self.content


    @property
    def content_remaining(self):
        s = self.content[self.start_index:]
        l = len(s)
        if l > self.MAX_CONTENT_LENGTH:
            remaining = l - self.MAX_CONTENT_LENGTH
            return '[%s more characters]' % remaining 
        return None


