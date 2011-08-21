from app_components.service import Service
from storage import StorageService
from models.tracker_group import TrackerGroup

class TrackerGroupService(StorageService):
    entity = TrackerGroup

    def get_all_by_user(self, user):
        return self.session.query(TrackerGroup).\
                filter(TrackerGroup.user_email == user.email).all()
