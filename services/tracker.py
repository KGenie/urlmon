import logging
from datetime import datetime, timedelta
from storage import StorageService
from models.tracker import Tracker
from models.tracker_group import TrackerGroup
from models.track_resource import TrackResource
from models.webpage import Webpage

__logger = logging.getLogger('services.tracker')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


class TrackerService(StorageService):

    entity = Tracker

    def after_insert(self, tracker):
        s = self.session
        t = TrackResource(tracker_id=tracker.id,\
            next_run=datetime.now() + timedelta(seconds=15))
        t.tracker = tracker
        s.add(t)


    def before_insert(self, tracker):
        if not tracker.css_selector:
            tracker.css_selector = 'body'
        s = self.session
        u = tracker.url
        if s.query(Webpage).filter(Webpage._url == u).count() == 0:
            wp = Webpage(url=tracker.url)
            # The merge is used in case of a race condition
            # (It will insert or update)
            tracker.webpage = wp


    def insert(self, tracker):
        self.before_insert(tracker)
        tracker = super(TrackerService, self).insert(tracker)
        self.after_insert(tracker)
        return tracker


    def before_delete(self, tracker):
        s = self.session
        tasks = s.query(TrackResource).filter(TrackResource.tracker_id ==
                tracker.id).all()
        if tasks:
            for task in tasks:
                s.delete(task)


    def delete(self, tracker):
        self.before_delete(tracker)
        ret = super(TrackerService, self).delete(tracker)
        return ret


    def any_with_group(self, group_id):
        return self.session.query(self.entity).\
                filter(Tracker.tracker_group_id == group_id).first()
      

    def get_all_by_user(self, user):
        return self.session.query(Tracker).join(TrackerGroup).\
                filter(TrackerGroup.user_id == user.id).all()


