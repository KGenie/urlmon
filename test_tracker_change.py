'''
Created on Mar 31, 2012

@author: bernard
'''

'''
Unit Test for Tracjer Change

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Be warned: produces many rows of data! 

'''
import env

from database.sqlalch import Session
from datetime import datetime
 
from models.registration import Registration
from models.task import Task
from models.tracker import Tracker
from models.tracker_change import TrackerChange
from models.tracker_group import TrackerGroup
from models.track_resource import TrackResource
from models.user import User
from models.webpage import Webpage
from models.webpage_version import WebpageVersion

from services.registration import RegistrationService
from services.tracker import TrackerService
from services.tracker_change import TrackerChangeService
from services.tracker_group import TrackerGroupService
from services.user import UserService
from services.webpage import WebpageService

from tests.services_handler import services_handler, service_data

from sqlalchemy import and_
from sqlalchemy import text

from time import time

import unittest

#########################################################################################



'''
Created on Mar 31, 2012

@author: bernard


'''

def create_tracker(session, arg_t, arg_object=None):
    t = Tracker()
    t.tracker_group_id = arg_t.tracker_group_id
    t.name = arg_t.name
    t.url = arg_t.url
    
    if t.tracker_group_id:
        print_number ("Group", t.tracker_group_id)
    else:
        print "No group"
        tg = TrackerGroup()
        t.tracker_group_id = create_user_and_tracker_group(session, tg)
        
    if not t.name:
        t.name = test_name()
    if not t.url:
        t.url = generate_url()
    create_webpage(session, t.url)
    my_service = TrackerService
    TrackerService(my_service).insert(t)
    session.flush()
    if arg_object:
        return t
    else:
        return t.id

def create_tracker_change(session, arg_tc, arg_object=None):
    tc = TrackerChange()
       
    tc.tracker_id = arg_tc.tracker_id
    tc.webpage_version_id = arg_tc.webpage_version_id   
    
    t = Tracker()
    
    if tc.tracker_id:
        my_result = session.query(Tracker).filter(Tracker.id == tc.tracker_id)
        my_url = my_result[0].url
    else:
        t = create_tracker(session, t, -1)
        my_url = t.url
        tc.tracker_id = t.id
    
    if not tc.webpage_version_id:
        tc.webpage_version_id = create_webpage_version(session, my_url)
         
    tc.content = test_prefix("Content")
    tc.digest = test_prefix("Digest")
    tc.current_css_selector = test_prefix("CSS")
    tc.current_css_selector = "body"
    tc.start_index = test_next()
    session.add(tc)
    session.flush()
    if arg_object:
    	return tc
    else:
    	return tc.id


def create_tracker_group (session, t):
       
# Needed for testing in several places.
    my_service = TrackerGroupService
    if not (t.name):
        t.name = test_name()
    TrackerGroupService(my_service).insert(t)
    session.flush();
    return t.id

def create_user (session, u):
# Needed for testing in several places.
    my_service = UserService
    
    if not (u.email):
        u.email = generate_email ();
    if not (u.first_name):
        u.first_name = "First"
    if not (u.last_name):
        u.last_name = test_name();
    
    UserService(my_service).insert(u)
    session.flush();
    return u.id

def create_user_and_tracker_group(session, t):
    u = User()
    my_id = create_user(session, u)
    t.user_id = my_id
    my_id = create_tracker_group(session, t)
    return my_id

def create_webpage(session, url):
    print "Checking " + url
    if not webpage_check(session, url):
        w = Webpage(url)
        w.url = url
        session.add(w)
        print "Created " + url
        
def create_webpage_version (session, arg_url=None, arg_content=None, arg_digest=None):
    if  not arg_url:
        arg_url = generate_url()
    create_webpage (session, arg_url)
    print "Creating version of " + arg_url
    wv = WebpageVersion(arg_url)
    if arg_content:
        wv.content = arg_content
    else:
        wv.content = test_prefix("Content")
    if arg_digest:
        wv.digest = arg_digest
    else:
        wv.digest = test_prefix("Digest")
    wv.datetime = datetime.now() 
    session.add(wv)
    session.flush()
    return wv.id    

def generate_email():
    return test_name_lc() + "@kgenie.com"

def generate_url():
    return "http://www.kgenie.com/" + test_name_lc()

 
def print_number (my_text, my_number):
# Prints text then a number. Handles number if null or non-numeric.
        if my_number:
            try:
                my_show = str(my_number)
            except:
                my_show = "None!"
        else:
            my_show = "None!"
        print my_text + ": " + my_show

def test_iteration():
# Holder for test name and number.
    null = 0
    
test_iteration.counter = 0
test_iteration.name = ""

def test_name(my_name=None):
# If Name supplied, change current test to supplied name.
    if my_name:
        test_iteration.name = my_name
        print " "
        print "Test: " + my_name
# Return test name appending unique number
    return test_iteration.name + "_" + str(test_next())

def test_name_lc ():
# Retrieve test name. Return in lower case with spaces converted to underscore. Intended to make this friendly as part of Email or URL
    my_name = test_name()
    my_name = my_name.lower()
    my_name = my_name.replace(" ", "_")
    return my_name

def test_next():
# Increment stored counter each time this is called.  
    test_iteration.counter = test_iteration.counter + 1
    return test_iteration.counter

def test_prefix(my_prefix):
# increment counter and return appended to supplied string.
    return my_prefix + "_" + str(test_next())

def webpage_check (session, my_url):
     if session.query(Webpage).filter(Webpage._url == my_url).count() == 0:
         return False
     else:
         return True
     



#########################################################################################

def run_once():
    session = Session()
    print "Initial reset"
    my_result = session.query(TrackResource).filter(TrackResource.tracker_id > 0)
    for my_row in my_result:
        session.delete(my_row)
        
    session.query(Task).filter(Task.id > 0).delete()
    session.query(TrackerChange).filter(TrackerChange.id > 0).delete()
    session.query(Tracker).filter(Tracker.id > 0).delete()
    
    session.query(WebpageVersion).filter(WebpageVersion.id > 0).delete()
    my_result = session.query(Webpage)
    for my_row in my_result:
        session.delete(my_row)
    
    session.query(TrackerGroup).filter(TrackerGroup.id > 0).delete()
    session.query(User).filter(User.id > 0).delete()
    
    my_result = session.query(Registration)
    for my_row in my_result:
        session.delete(my_row)
    
    
    session.commit()
    

class testing(unittest.TestCase):

    def setUp(self):

        self.session = Session()
              
    def tearDown(self):
        try:
            self.session.commit()
            print test_name() + " committed"
        except:
            print test_name() + " commit failed" 
            self.assertTrue(0)
            
    def xtest_get_change_base_query_tracker(self):
        test_name("Get change base query tracker")
        
        version_id = create_webpage_version(self.session)
    
        t = Tracker()
        tracker_1 = create_tracker(self.session, t)
        
        print_number("Tracker", tracker_1)
        
        tc = TrackerChange()
        tc.tracker_id = tracker_1
        tc.webpage_version_id = version_id
        create_tracker_change(self.session, tc)
        my_service = TrackerChangeService
        
        t = Tracker()
        t.id = tracker_1
        my_result = TrackerChangeService(my_service).get_change_base_query(None, None, t)
        self.assertEqual(tracker_1, my_result[0].id)
    
    
    def xtest_get_change_base_query_tracker_group(self):
        test_name("Get change base query group")
        
        
        version_id = create_webpage_version(self.session)
    
        tg = TrackerGroup()
    
        tracker_group_id = create_tracker_group(self.session, tg)
    
        t = Tracker()
        t.tracker_group_id = tracker_group_id
        tracker_1 = create_tracker(self.session, t)
        
        t = Tracker()
        t.tracker_group_id = tracker_group_id
        tracker_2 = create_tracker(self.session, t)
       
        tc = TrackerChange()
        tc.tracker_id = tracker_1
        tc.webpage_version_id = version_id
        create_tracker_change(self.session, tc)
        
        tc = TrackerChange()
        tc.tracker_id = tracker_2
        tc.webpage_version_id = version_id
        create_tracker_change(self.session, tc)
        
        my_service = TrackerChangeService
        
        tg = TrackerGroup()
        tg.id = tracker_group_id
        my_result = TrackerChangeService(my_service).get_change_base_query(None, tg, None)
        self.assertEqual(tracker_1, my_result[0].id)
        self.assertEqual(tracker_2, my_result[1].id)
       
    def test_get_new_page(self):   
# Context problems prevent testing.
        test_name("Get new page")
        t = Tracker()
        t = create_tracker(self.session,t,-1)
        tracker_id = t.id
        my_url = t.url
        my_content = test_prefix("Content")
        my_digest = test_prefix("Digest")
        wv_id = create_webpage_version (self.session,my_url, my_content, my_digest)
        tc = TrackerChange()
        tc.tracker_id = tracker_id
        tc.webpage_version_id = wv_id
        tc = create_tracker_change(self.session, tc, -1)
        my_service = TrackerChangeService
        my_result = TrackerChangeService(my_service).get_new_page(tc)
        my_expected = "<p>" + my_content + "</p>\n"
        self.assertEqual(my_result, my_expected)
		
    def test_get_previous_page(self):   
        test_name("Get previous page")
        t = Tracker()
        t = create_tracker(self.session,t,-1)
        tracker_id = t.id
        my_url = t.url
        my_content = test_prefix("Content")
        my_digest = test_prefix("Digest")
        wv_id = create_webpage_version (self.session,my_url, my_content, my_digest)
        tc = TrackerChange()
        tc.tracker_id = tracker_id
        tc.webpage_version_id = wv_id
        tc = create_tracker_change(self.session, tc, -1)
        my_service = TrackerChangeService
        my_result = TrackerChangeService(my_service).get_previous_page(tc)
        my_expected = "<p>" + my_content + "</p>\n"
        self.assertEqual(my_result, my_expected)
        
    def test_get_previous_pages(self):   
        test_name("Get previous pages")
        t = Tracker()
        t = create_tracker(self.session,t,-1)
        tracker_id = t.id
        my_url = t.url
        
        my_content = test_prefix("Content1")
        my_digest = test_prefix("Digest1")
        wv_id = create_webpage_version (self.session,my_url, my_content, my_digest)
        tc = TrackerChange()
        tc.tracker_id = tracker_id
        tc.webpage_version_id = wv_id
        tc = create_tracker_change(self.session, tc, -1)
        
        my_content = test_prefix("Content2")
        my_digest = test_prefix("Digest2")
        wv_id = create_webpage_version (self.session,my_url, my_content, my_digest)
        tc = TrackerChange()
        tc.tracker_id = tracker_id
        tc.webpage_version_id = wv_id
        tc = create_tracker_change(self.session, tc, -1)
        
        my_service = TrackerChangeService
        my_result = TrackerChangeService(my_service).get_previous_page(tc)
        my_expected = "<p>" + my_content + "</p>\n"
        print my_expected
        print my_result
        self.assertEqual(my_result, my_expected)
        
        
run_once()    
    
if __name__ == '__main__':
    unittest.main()
