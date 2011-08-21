from app_components.model import Model, TableModel
from forms.tracker_group import TrackerGroupForm

class TrackerGroup(Model):

    def __init__(self, name=None, comment=None, user_email=None):
        self.name = name
        self.comment = comment
        self.user_email = user_email

class TrackerGroupTable(TableModel):

    form = TrackerGroupForm
