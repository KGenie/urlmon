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
        tracker_groups = self.tracker_group_service.get_all_by_user(self.session['user'])
        return self.view({'tracker_groups': tracker_groups, 'form': form})



    @get
    @menu(label='Create a Tracker Group')
    def new(self, request):
        form = TrackerGroupForm()
        return self.view({'form': form})


    @get
    @menu(exclude=True)
    def edit(self, request):
        id = request.GET.get('id', None)
        if not id:
            return self.redirect('index')
        tracker_group = self.tracker_group_service.get(id)
        form = TrackerGroupForm(obj=tracker_group)
        return self.view({'form': form, 'id': id})


    @post
    def update(self, request):
        form = TrackerGroupForm(request.POST)
        if form.validate():
            id = request.POST.get('id', None)
            tracker_group = TrackerGroup()
            form.populate_obj(tracker_group)
            tracker_group.user = self.session['user'].email
            self.tracker_group_service.update(id, tracker_group)
            return self.redirect('index')

        return self.view({'form':form}, 'edit')


    @post
    def create(self, request):
        form = TrackerGroupForm(request.POST)
        if form.validate():
            tracker_group = TrackerGroup()
            form.populate_obj(tracker_group)
            tracker_group.user = self.session['user'].email
            self.tracker_group_service.insert(tracker_group)
            return self.redirect('index')

        return self.view({'form':form}, 'new')
