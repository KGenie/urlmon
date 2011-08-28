from hashlib import sha1
from app_components.model import Model

class TrackerChangeView(Model):

    def __init__(self, tracker_change, now):
        self.id = tracker_change.id
        self.tracker_id = tracker_change.tracker.id
        self.tracker_url = tracker_change.tracker.webpage.url
        self.tracker_name = tracker_change.tracker.name
        self.tracker_url_short = self.tracker_url
        self.content = tracker_change.content
        self.date = tracker_change.webpage_version.date
        self.now = now

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


