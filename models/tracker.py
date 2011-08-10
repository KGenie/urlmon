from app_components.model import Model
from app_components.model import TableModel
from forms.tracker import TrackerForm


class Tracker(Model):

    def __init__(self, id=None, name=None, url=None, frequency=None, 
            tracker_group_id=None, css_selector=None, user_id=None):
        self.id = id
        self.name = name
        self.url = url
        self.frequency = frequency
        self.tracker_group_id = tracker_group_id
        self.css_selector = css_selector
        self.user_id = user_id



class TrackerTable(TableModel):

    form = TrackerForm
    exclude = [
            'tracker_group_id'
            ]
    include = [
            ('tracker_group.name', 'Tracker group')
            ]
