from datetime import datetime
from app_components.controller import WebMonitorController
from models.tracker_change_view import TrackerChangeView
from services.tracker import TrackerService
from services.tracker_change import TrackerChangeService
from services.tracker_group import TrackerGroupService
from wsgi.http_method import get, post
from helpers import menu


class TrackerChangeController(WebMonitorController):

    tracker_service = TrackerService
    tracker_change_service = TrackerChangeService
    tracker_group_service = TrackerGroupService

    @get
    @menu(exclude=True)
    def index(self, request):
        page = request.GET.get('page', 1)
        tracker_id = request.GET.get('tracker_id', None)
        if tracker_id:
            tracker_id = int(tracker_id)

        page = int(page)
        id = request.GET.get('id', None)
        if id:
            tracker_group = self.tracker_group_service.get(id)
        else:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_group.user.id != current_user_id:
            return self.forbidden()
         
        now = datetime.now()
        count = self.tracker_change_service.get_change_count(tracker_group,
                tracker_id)

        maxpage = count / 5
        if count % 5 != 0:
            maxpage += 1

        if page > maxpage:
            return self.notfound()

        changes = self.tracker_change_service.get_changes(tracker_group, 
                page, tracker_id)
        trackers = self.tracker_service.get_all_by_group(tracker_group)
        
        results = (TrackerChangeView(c, now) for c in changes)
        return self.view({'changes': results, 'page' : page, 
            'maxpage': maxpage, 'id': id, 'trackers': trackers, 
            'tracker_id': tracker_id  })

    @get
    @menu(exclude=True)
    def new_content(self, request):
        id = request.GET.get('id', None)
        if id:
            tracker_change = self.tracker_change_service.get(id)
        else:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_change.tracker.tracker_group.user.id != current_user_id:
            return self.forbidden()

        new = tracker_change.webpage_version.content
        return self.content(new)


    @get
    @menu(exclude=True)
    def change_content(self, request):
        id = request.GET.get('id', None)
        if id:
            tracker_change = self.tracker_change_service.get(id)
        else:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_change.tracker.tracker_group.user.id != current_user_id:
            return self.forbidden()

        return self.content(tracker_change.content)


    @get
    @menu(exclude=True)
    def old_content(self, request):
        id = request.GET.get('id', None)
        if id:
            tracker_change = self.tracker_change_service.get(id)
        else:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_change.tracker.tracker_group.user.id != current_user_id:
            return self.forbidden()

        old = tracker_change.webpage_version.content
        return self.content(old)


    @get
    @menu(exclude=True)
    def diff(self, request):
        id = request.GET.get('id', None)
        if id:
            tracker_change = self.tracker_change_service.get(id)
        else:
            return self.notfound()

        current_user_id = self.session['user'].id
        if tracker_change.tracker.tracker_group.user.id != current_user_id:
            return self.forbidden()

        diffed_content = self.tracker_change_service\
                .get_page_diff(tracker_change)

        return self.content(diffed_content)
