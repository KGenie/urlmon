from storage import StorageService
from models.tracker_group import TrackerGroup

class TrackerGroupService(StorageService):
    entity = TrackerGroup

    def get_all_by_user(self, user):
        return self.session.query(TrackerGroup).\
                filter(TrackerGroup.user_id == user.id).all()


    def exists_with_name(self, name):
        user = self.context.environ['beaker.session']['user']
        return bool(self.session.query(TrackerGroup).\
                filter(TrackerGroup.user_id == user.id).\
                filter(TrackerGroup.name == name).first())

        