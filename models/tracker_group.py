from app_components.model import Model, TableModel
from forms.tracker_group import TrackerGroupForm

class TrackerGroup(Model):

    def __init__(self, name=None, comment=None, user_id=None):
        self.name = name
        self.comment = comment
        self.user_id = user_id

class TrackerGroupTable(TableModel):

    form = TrackerGroupForm
