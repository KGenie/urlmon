from app_components.controller import WebMonitorController
from models.tracker_group import TrackerGroup
from models.tracker_change_view import TrackerChangeView
from forms.tracker_group import TrackerGroupForm
from services.tracker_group import TrackerGroupService
from services.tracker import TrackerService
from wsgi.http_method import get, post
from helpers import menu
from database.sqlalch import Session

@menu(label='Tracker Groups')
class TrackerGroupController(WebMonitorController):

    tracker_group_service = TrackerGroupService
    tracker_service = TrackerService


    @get
    @menu(label='Manage')
    def index(self, request):
        tracker_groups = self.tracker_group_service.get_all_by_user(self.session['user'])
        return self.view({'tracker_groups': tracker_groups})



    @get
    @menu(label='Create')
    def new(self, request):
        form = TrackerGroupForm()
        return self.view({'form': form})



    @get
    @menu(exclude=True)
    def edit(self, request):
        id = request.GET.get('id', None)
        if not id:
            self.session['flash-error'] = 'An id must be specified'
            return self.redirect('index')
        tracker_group = self.tracker_group_service.get(id)

        if not tracker_group:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_group.user.id != current_user_id:
            return self.forbidden()

        form = TrackerGroupForm(obj=tracker_group)
        return self.view({'form': form})


    @get
    @menu(exclude=True)
    def confirm_delete(self, request):
        id = request.GET.get('id', None)
        if not id:
            self.session['flash-error'] = 'An id must be specified'
            return self.redirect('index')

        if self.tracker_service.any_with_group(id):
            self.session['flash-error'] =\
                    'This group can''t be deleted, as it contains one or more trackers.'
            return self.redirect('index')


        tracker_group = self.tracker_group_service.get(id)

        if not tracker_group:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_group.user.id != current_user_id:
            return self.forbidden()


        form = TrackerGroupForm(obj=tracker_group)
        return self.view({'form': form})

    @post
    def create(self, request):
        form = TrackerGroupForm(request.POST)
        setattr(form, '_check_name', True)
        setattr(form, '_tracker_group_service', self.tracker_group_service)

        if form.validate():
            tracker_group = TrackerGroup()
            form.populate_obj(tracker_group)
            tracker_group.user_id = self.session['user'].id
            tracker_group = self.tracker_group_service.insert(tracker_group)
            if not tracker_group:
                self.session['flash-error'] = \
                'There was a server error while trying to create the tracker group'
            else:
                self.session['flash-success'] = \
                'Tracker group sucessfully created'

            return self.redirect('index')

        return self.view({'form':form}, 'new')


    @post
    def update(self, request):
        form = TrackerGroupForm(request.POST)
        id = form.id.data
        tracker_group = self.tracker_group_service.get(id)
        if not tracker_group:
            return self.notfound()
        if form.name.data != tracker_group.name:
            setattr(form, '_check_name', True)

        setattr(form, '_tracker_group_service', self.tracker_group_service)
        if form.validate():
         
            form.populate_obj(tracker_group)
            current_user_id = self.session['user'].id

            if tracker_group.user.id != current_user_id:
                return self.forbidden()

            tracker_group = self.tracker_group_service.update(tracker_group.id, tracker_group)
            if not tracker_group:
                self.session['flash-error'] = \
                'There was a server error while trying to update the tracker group'
            else:
                self.session['flash-success'] = \
                'Tracker group sucessfully updated'

            return self.redirect('index')

        return self.view({'form':form}, 'edit')


    @post
    def delete(self, request):
        id = request.POST.get('id', None)
        tracker_group = self.tracker_group_service.get(id)

        if not tracker_group:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_group.user.id != current_user_id:
            return self.forbidden()

        rows = self.tracker_group_service.delete(tracker_group)
        if not rows:
            self.session['flash-error'] = \
            'There was an error while trying to delete the tracker group'
        else:
            self.session['flash-success'] =\
            'Tracker group sucessfully deleted'

        return self.redirect('index')





