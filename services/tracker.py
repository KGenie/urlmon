from datetime import datetime, timedelta
from storage import StorageService
from models.tracker import Tracker
from models.tracker_group import TrackerGroup
from models.update_resource import UpdateResource
from models.track_resource import TrackResource


class TrackerService(StorageService):

    entity = Tracker

    def on_update(self, tracker):
        s = self.session
        t1 = UpdateResource(url=tracker.url,
            next_run=datetime.now() + timedelta(seconds=5))
        t2 = TrackResource(tracker_id=tracker.id,\
            next_run=datetime.now() + timedelta(seconds=15))
        t2.tracker = tracker
        s.add_all([t1,t2])


  
    def insert(self, tracker):
        tracker = super(TrackerService, self).insert(tracker)
        self.on_update(tracker)
        return tracker


    def any_with_group(self, group_id):
        return self.session.query(self.__class__).\
                filter(Tracker.tracker_group_id == group_id).first()
      

    def get_all_by_user(self, user):
        return self.session.query(Tracker).join(TrackerGroup).\
                filter(TrackerGroup.user_email == user.email).all()

