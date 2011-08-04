from app_components.controller import WebMonitorController
from models.tracker import Tracker
from forms.tracker import TrackerForm
from services.tracker import TrackerService
from wsgi.http_method import get, post

class TrackerController(WebMonitorController):

    tracker_service = TrackerService

    @get
    def index(self, request):
        form = TrackerForm()
        trackers = self.tracker_service.get_all(self.session['user'])

        return self.view({'form': form, 'trackers': trackers})

       
    @post
    def create(self, request):
        form = TrackerForm(request.POST)
        if form.validate():
            tracker = Tracker()
            form.populate_obj(tracker)
            tracker.user = self.session['user']
            self.tracker_service.insert(tracker)
            return self.redirect('index')

        return self.view({'form':form }, 'index')
