from app_components.controller import WebMonitorController
from models.tracker_group import TrackerGroup
from forms.tracker_group import TrackerGroupForm
from services.tracker_group import TrackerGroupService
from wsgi.http_method import get, post
from helpers import menu

@menu(label='Tracker Groups')
class TrackerGroupController(WebMonitorController):

    tracker_group_service = TrackerGroupService

    @get
    @menu(label='Manage Tracker Groups')
    def index(self, request):
        form = TrackerGroupForm()
        tracker_groups = self.tracker_group_service.get_all(self.session['user'])

        return self.view({'form': form, 'tracker_groups': tracker_groups})


    @post
    def create(self, request):
        form = TrackerGroupForm(request.POST)
        if form.validate():
            tracker_group = TrackerGroup()
            form.populate_obj(tracker_group)
            tracker_group.user = self.session['user']
            self.tracker_group_service.insert(tracker_group)
            return self.redirect('index')

        return self.view({'form':form}, 'index')

