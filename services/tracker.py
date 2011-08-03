from app_components.service import Service

trackers = []

class TrackerService(Service):

    def insert(self, tracker):
        trackers.append(tracker)


    def get_all(self, user):
        return (t for t in trackers if t.user == user)
