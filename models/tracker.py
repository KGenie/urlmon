from util import normalize_url
from app_components.model import Model
from app_components.model import TableModel
from forms.tracker import TrackerForm


class Tracker(Model):

    def __init__(self, name=None, url=None, frequency=None,
            tracker_group_id=None, css_selector=None, comment=None):
        self.name = name
        self.url = url
        self.frequency = frequency
        self.tracker_group_id = tracker_group_id
        self.css_selector = css_selector
        self.comment = comment
        
       


    @property
    def url(self):
        return self._url


    @url.setter
    def url(self, value):
        if value:
            self._url = normalize_url(value)
        else:
            self._url = None



class TrackerTable(TableModel):

    form = TrackerForm
    exclude = [
            'tracker_group_id',
            'comment'
            ]
    include = [
            ('tracker_group.name', 'Tracker group')
            ]
