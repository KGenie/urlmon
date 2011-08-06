from app_components.service import Service
from storage import StorageService
from models.tracker import Tracker


class TrackerService(StorageService):


    @classmethod
    def stub_data(cls):
        cls.insert(Tracker(name='Google tracker', url='http://www.google.com',
            tracker_group='Search engines', frequency='20',
            user='tap'))
        cls.insert(Tracker(name='Yahoo tracker', url='http://www.yahoo.com',
            tracker_group='Search engines', frequency='5',
            user='tap'))

