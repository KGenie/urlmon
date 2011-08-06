from app_components.service import Service
from storage import StorageService
from tracker_group import TrackerGroupService
from models.tracker import Tracker


class TrackerService(StorageService):


    @classmethod
    def stub_data(cls):
        cls.insert(Tracker(name='Google tracker', url='http://www.google.com',
            tracker_group_id=1, frequency='20',
            user_id=1))
        cls.insert(Tracker(name='Yahoo tracker', url='http://www.yahoo.com',
            tracker_group_id=1, frequency='5',
            user_id=1))


    @classmethod
    def get_all(cls):
        all = super(TrackerService, cls).get_all()
        for item in all:
            id = item.tracker_group_id
            tracker_group = TrackerGroupService(None).get(id)
            setattr(item, 'tracker_group', tracker_group)
        return super(TrackerService, cls).get_all()

    @classmethod
    def any_with_group(cls, group_id):
        group_id = int(group_id)
        l = list(t for t in cls.get_all() if t.tracker_group_id == group_id)
        return len(l)
