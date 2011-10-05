import logging
from storage import StorageService
from models.tracker_change import TrackerChange
from models.tracker import Tracker
from lxml import etree, html
from lxml.html import builder as E
from lxml.html.diff import htmldiff
from helpers import UrlHelper
from daemons.webpage import select_content
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


    def get_change_count(self, tracker_group, tracker_id):
        s = self.session

        if tracker_id:
            tracker_ids_query = s.query(Tracker.id)\
                    .filter(Tracker.id == tracker_id)
        else:
            tracker_ids_query = s.query(Tracker.id)\
                    .filter(Tracker.tracker_group_id == tracker_group.id)

        return s.query(TrackerChange)\
                .filter(TrackerChange.tracker_id.in_(tracker_ids_query))\
                .count()


    def get_changes(self, tracker_group, page, page_size, tracker_id):
        first = ((page - 1) * page_size) + 1
        s = self.session

        if tracker_id:
            tracker_ids_query = s.query(Tracker.id)\
                    .filter(Tracker.id == tracker_id)
        else:
            tracker_ids_query = s.query(Tracker.id)\
                    .filter(Tracker.tracker_group_id == tracker_group.id)

        return s.query(TrackerChange)\
                .filter(TrackerChange.tracker_id.in_(tracker_ids_query))\
                .order_by(TrackerChange.id.desc())\
                .limit(page_size)\
                .offset(first)\
                .all()


    def get_last_two_changes(self, tracker_change):
        s = self.session

        last_two_changes = s.query(TrackerChange)\
                .filter(TrackerChange.id <= tracker_change.id)\
                .filter(TrackerChange.tracker_id == tracker_change.tracker.id)\
                .order_by(TrackerChange.id.desc())\
                .limit(2).all()

        assert len(last_two_changes) >= 1 and \
                last_two_changes[0].id == tracker_change.id, 'Inconsistent db'
        return last_two_changes




    def get_new_page(self, tracker_change):
        #dom = html.fromstring(tracker_change.webpage_version.content)
        #select_content(dom, tracker_change.tracker.css_selector)
        #return etree.tostring(dom)
        return tracker_change.webpage_version.content
    


    def get_previous_page(self, tracker_change):
        last_two_changes = self.get_last_two_changes(tracker_change)
        if len(last_two_changes) == 2:
            warn('OK')
            version = last_two_changes[1].webpage_version
        else:
            warn('ERRR')
            version = last_two_changes[0].webpage_version

        #FIXME 'select_content' function is breaking html
        #dom = html.fromstring(version.content)
        #select_content(dom, tracker_change.tracker.css_selector)
        #return etree.tostring(dom)
        return version.content


    def get_page_diff(self, tracker_change):
        last_two_changes = self.get_last_two_changes(tracker_change)

        new_version = tracker_change.webpage_version
        if len(last_two_changes) == 2:
            return diff(last_two_changes[1].webpage_version, new_version,
                    tracker_change.tracker.css_selector)
        else:
            return new_version.content
