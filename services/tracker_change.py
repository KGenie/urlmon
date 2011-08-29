import cgi
from storage import StorageService
from models.tracker_change import TrackerChange
from models.tracker import Tracker
from lxml import etree, html
from lxml.html import builder as E
from lxml.html.diff import htmldiff
from helpers import UrlHelper
from daemons.webpage import select_content

u = UrlHelper()

def diff(old_version, new_version, css_selector):
    dom = html.fromstring(new_version.content)
    diffed = htmldiff(old_version.content, new_version.content)
    diffed_dom = html.fromstring(diffed)
       
    dom.body.clear()
    dom.body.append(diffed_dom)

    dom.append(E.LINK(rel='stylesheet', type='text/css',\
            href=u.static('/css/diff.css')))
    dom.append(E.LINK(rel='stylesheet', type='text/css',\
            href=u.static('/css/frame.css')))
    select_content(dom, css_selector)

    return etree.tostring(dom)


class TrackerChangeService(StorageService):
    entity = TrackerChange

    def get_changes(self, tracker_group):
        s = self.session

        tracker_ids_query = s.query(Tracker.id)\
                .filter(Tracker.tracker_group_id == tracker_group.id)

        return s.query(TrackerChange)\
                .filter(TrackerChange.tracker_id.in_(tracker_ids_query))\
                .order_by(TrackerChange.id.desc())\
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
        dom = html.fromstring(tracker_change.webpage_version.content)
        select_content(dom, tracker_change.tracker.css_selector)
        return etree.tostring(dom)
    


    def get_previous_page(self, tracker_change):
        last_two_changes = self.get_last_two_changes(tracker_change)
        if len(last_two_changes) == 2:
            version = last_two_changes[1].webpage_version
        else:
            version = last_two_changes[0].webpage_version

        dom = html.fromstring(version.content)
        select_content(dom, tracker_change.tracker.css_selector)
        return etree.tostring(dom)


    def get_page_diff(self, tracker_change):
        last_two_changes = self.get_last_two_changes(tracker_change)

        new_version = tracker_change.webpage_version
        if len(last_two_changes) == 2:
            return diff(last_two_changes[1].webpage_version, new_version,
                    tracker_change.tracker.css_selector)
        else:
            return new_version.content
