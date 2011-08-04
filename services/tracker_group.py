from app_components.service import Service

tracker_groups = []

class TrackerGroupService(Service):

    def insert(self, tracker_group):
        tracker_groups.append(tracker_group)


    def get_all(self, user):
        return (t for t in tracker_groups if t.user == user)
