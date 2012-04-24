import logging
from storage import StorageService
from models.tracker_change import TrackerChange
from models.tracker import Tracker
from models.tracker_group import TrackerGroup
from models.webpage_version import WebpageVersion
from lxml import etree, html
from lxml.html import builder as E
from lxml.html.diff import htmldiff
from helpers import UrlHelper
from daemons.webpage import select_content, highlight_selected
from htmldiff import htmldiff, change_start_index

u = UrlHelper()

__logger = logging.getLogger('services.tracker_change')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info



def diff(old_version, new_version, css_selector):
    return htmldiff(old_version.content, new_version.content, True)


class TrackerChangeService(StorageService):
    entity = TrackerChange


    def get_change_base_query(self, user, tracker_group, tracker):
        s = self.session

        tracker_ids_query = s.query(Tracker.id)

        if tracker:
            tracker_ids_query = tracker_ids_query\
                    .filter(Tracker.id == tracker.id)

        elif tracker_group:
            tracker_ids_query = tracker_ids_query\
                    .filter(Tracker.tracker_group_id == tracker_group.id)

        else:
            tracker_ids_query = tracker_ids_query.join(TrackerGroup)\
                    .filter(TrackerGroup.user_id == user.id)

        return s.query(TrackerChange).join(WebpageVersion)\
                .filter(TrackerChange.tracker_id.in_(tracker_ids_query))



    def get_changes(self, user, tracker_group=None, tracker=None, page_size=10,
            page=1):
        
        first = ((page - 1) * page_size) + 1
        base_query = self.get_change_base_query(user, tracker_group, tracker)

        return base_query.order_by(WebpageVersion.date.desc())\
                .limit(page_size)\
                .offset(first - 1)\
                .all()


    def get_change_count(self, user, tracker_group, tracker):
        base_query = self.get_change_base_query(user, tracker_group, tracker)
        return base_query.count()



    def get_last_two_changes(self, tracker_change):
        print "GLTC"
        print tracker_change.id
        print tracker_change.tracker_id
        
        s = self.session

        last_two_changes = s.query(TrackerChange).join(WebpageVersion)\
                .filter(TrackerChange.id <= tracker_change.id)\
                .filter(TrackerChange.tracker_id == tracker_change.tracker.id)\
                .order_by(WebpageVersion.date.desc())\
                .limit(2).all()
        
        print last_two_changes[0].id
        try:
            print last_two_changes[1].id
        except:
            print "no more"
        
   #     assert len(last_two_changes) >= 1 and \
   #             last_two_changes[0].id == tracker_change.id, 'Inconsistent db'
        return last_two_changes



    def get_new_page(self, tracker_change):
        dom = html.fromstring(tracker_change.webpage_version.content)
        selector = tracker_change.current_css_selector
        select_content(dom, selector)
        highlight_selected(dom, selector)
        return etree.tostring(dom,method='html', pretty_print=True)
    


    def get_previous_page(self, tracker_change):
        last_two_changes = self.get_last_two_changes(tracker_change)
        if len(last_two_changes) == 2:
            warn('OK')
            version = last_two_changes[1].webpage_version
        else:
            warn('ERRR')
            version = last_two_changes[0].webpage_version

        #FIXME 'select_content' function is breaking html
        dom = html.fromstring(version.content)
        selector = tracker_change.current_css_selector
        select_content(dom, selector)
        highlight_selected(dom, selector)
        return etree.tostring(dom, method='html', pretty_print=True)


    def get_page_diff(self, tracker_change):
        last_two_changes = self.get_last_two_changes(tracker_change)

        new_version = tracker_change.webpage_version

        if len(last_two_changes) == 2:
            html_diff = diff(last_two_changes[1].webpage_version, new_version,
                    tracker_change.tracker.css_selector)
        else:
            html_diff = new_version.content

        dom = html.fromstring(html_diff)
        selector = tracker_change.current_css_selector
        select_content(dom, selector)
        highlight_selected(dom, selector)
        return etree.tostring(dom, method='html', pretty_print=True)
