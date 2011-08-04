from app_components.controller import WebMonitorController
from models.tracker import Tracker
from forms.tracker import TrackerForm
from services.tracker import TrackerService
from services.tracker_group import TrackerGroupService
from wsgi.http_method import get, post
from helpers import menu

@menu(label='Trackers')
class TrackerController(WebMonitorController):

    tracker_service = TrackerService
    tracker_group_service = TrackerGroupService

    @get
    @menu(label='Manage Trackers')
    def index(self, request):
        tracker_groups = ((tg.name,tg.name) for tg in
                self.tracker_group_service.get_all(self.session['user']))
        form = TrackerForm()
        form.tracker_groups.choices = tracker_groups

        trackers = self.tracker_service.get_all(self.session['user'])

        return self.view({'form': form, 'trackers': trackers})


    @post
    def create(self, request):
        form = TrackerForm(request.POST)
        tracker_groups = ((tg.name,tg.name) for tg in
        self.tracker_group_service.get_all(self.session['user']))
        form.tracker_groups.choices = tracker_groups

        if form.validate():
            tracker = Tracker()
            form.populate_obj(tracker)
            tracker.user = self.session['user']
            self.tracker_service.insert(tracker)
            return self.redirect('index')

        return self.view({'form':form }, 'index')

