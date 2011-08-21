from datetime import datetime, timedelta
from storage import StorageService
from models.tracker import Tracker


class TrackerService(StorageService):

    entity = Tracker

  
    def insert(self, tracker):
        tracker = super(TrackerService, self).insert(tracker)
        self.session.refresh(tracker)
        self.session.add(UpdateResource(url=tracker.url,
            next_run=datetime.now() + timedelta(seconds=20)))
        self.session.add(TrackResource(tracker_id=tracker.id,\
            next_run=datetime.now() + timedelta(seconds=5)))
        return tracker


    def any_with_group(self, group_id):
        return self.session.query(self.__class__).\
                filter(Tracker.tracker_group_id == group_id).first()
      

    def get_all_by_user(self, user):
        return self.session.query(Tracker).\
                filter(Tracker.user_email == user.email).all()

