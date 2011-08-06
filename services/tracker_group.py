from app_components.service import Service
from storage import StorageService
from models.tracker_group import TrackerGroup

class TrackerGroupService(StorageService):

    @classmethod
    def stub_data(cls):
        cls.insert(TrackerGroup(name='Search engines', user='tap',
            comment='Trackers for search engines.'))
