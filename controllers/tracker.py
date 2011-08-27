from datetime import datetime, timedelta
from app_components.controller import WebMonitorController
from models.tracker import Tracker, TrackerTable
from models.update_resource import UpdateResource
from models.track_resource import TrackResource
from forms.tracker import TrackerForm
from services.tracker import TrackerService
from services.tracker_group import TrackerGroupService
from services.task import TaskService
from services.fetcher import FetcherService
from wsgi.http_method import get, post
from helpers import menu
from database.sqlalch import Session

@menu(label='Trackers')
class TrackerController(WebMonitorController):

    tracker_service = TrackerService
    tracker_group_service = TrackerGroupService
    fetcher_service = FetcherService


    @get
    @menu(label='Manage')
    def index(self, request):
        trackers = self.tracker_service.get_all_by_user(self.session['user'])
        table = TrackerTable(trackers)
        return self.view({'table_model': table})


    @get
    @menu(label='Create')
    def new(self, request):
        form = self.create_form()
        return self.view({'form':form })


    @get
    @menu(exclude=True)
    def edit(self, request):
        id = request.GET.get('id', None)
        if not id:
            return self.redirect('index')
        tracker = self.tracker_service.get(id)
        if not tracker:
            return self.notfound()
        current_user_id = self.session['user'].id
        if tracker.tracker_group.user.id != current_user_id:
            return self.forbidden()


        form = self.create_form(obj=tracker)

        return self.view({'form': form})


    @get
    @menu(exclude=True)
    def confirm_delete(self, request):
        id = request.GET.get('id', None)
        if not id:
            return self.redirect('index')
        tracker = self.tracker_service.get(id)

        if not tracker:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker.tracker_group.user.id != current_user_id:
            return self.forbidden()


        form = self.create_form(obj=tracker)
        tracker_group =\
                self.tracker_group_service.get(tracker.tracker_group_id)
        form.tracker_group_id.data = tracker_group.name
        return self.view({'form': form})

   
    @get
    @menu(exclude=True)
    def cached_url(self, request):
        url = request.GET.get('url', None)
        selector = request.GET.get('selector', None)
        if not url:
            return None
        page = self.fetcher_service.fetch(url, selector)
        if not page:
            return self.content('Server error ocurred!')
        return self.content(page.content)


    @post
    def create(self, request):
        form = self.create_form(request.POST)

        if form.validate():
            tracker = Tracker()
            form.populate_obj(tracker)
            tracker = self.tracker_service.insert(tracker)


            return self.redirect('index')

        return self.view({'form':form }, 'new')

   
    @post
    def update(self, request):
        form = self.create_form(request.POST)
        if form.validate():
            id = form.id.data
            tracker = self.tracker_service.get(id)
            if not tracker:
                return self.notfound()

            form.populate_obj(tracker)
            current_user_id = self.session['user'].id

            if tracker.tracker_group.user.id != current_user_id:
                return self.forbidden()

            tracker = self.tracker_service.update(tracker.id, tracker)
            if not tracker:
                self.session['flash-error'] = \
                'There was a server error while trying to update the tracker'
            else:
                self.session['flash-success'] = \
                'Tracker sucessfully updated'

            return self.redirect('index')

        return self.view({'form':form}, 'edit')


    @post
    def delete(self, request):
        id = request.POST.get('id', None)
        tracker = self.tracker_service.get(id)

        if not tracker:
            return self.notfound()


        current_user_id = self.session['user'].id
        if tracker.tracker_group.user.id != current_user_id:
            return self.forbidden()


        rows = self.tracker_service.delete(tracker)
        if not rows:
            self.session['flash-error'] = \
            'There was an error while trying to delete the tracker'
        else:
            self.session['flash-success'] =\
            'Tracker sucessfully deleted'

        return self.redirect('index')


    def create_form(self, data=None, obj=None):
        form = TrackerForm(data, obj=obj)
        tracker_groups = list((tg.id,tg.name) for tg in
                self.tracker_group_service.get_all_by_user(self.session['user']))
        form.tracker_group_id.choices = tracker_groups
        return form
