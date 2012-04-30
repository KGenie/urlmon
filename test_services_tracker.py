'''
Created on Mar 31, 2012

@author: bernard
'''

'''
Unit Test for Services.

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Be warned: produces many rows of data! 

'''
import env

from database.sqlalch import Session
 
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
def create_tracker_group (session,t):
       
# Needed for testing in several places.
    my_service = TrackerGroupService
    if not (t.name):
        t.name = test_name()
    TrackerGroupService(my_service).insert(t)
    session.flush();
    return t.id

def create_user (session,u):
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

def create_user_and_tracker_group(session,t):
    u = User()
    my_id = create_user(session,u)
    t.user_id = my_id
    my_id = create_tracker_group(session,t)
    return my_id

def generate_email():
    return test_name_lc() + "@kgenie.com"

def generate_url():
    return "http://www.kgenie.com/" + test_name_lc()

 
def print_number (my_text,my_number):
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
# Return test name appending unique number
    return test_iteration.name + "_" + str(test_next())

def test_name_lc ():
# Retrieve test name. Return in lower case with spaces converted to underscore. Intended to make this friendly as part of Email or URL
    my_name = test_name()
    my_name = my_name.lower()
    my_name = my_name.replace(" ","_")
    return my_name

def test_next():
# Increment stored counter each time this is called.  
    test_iteration.counter = test_iteration.counter + 1
    return test_iteration.counter

def test_suffix(my_suffix):
# increment counter and return appended to supplied string.
    return my_suffix + "_" + str(test_next())

def webpage_check (session,my_url):
     if session.query(Webpage).filter(Webpage._url == my_url).count() == 0:
         return False
     else:
         return True
     
def webpage_create(session,url):
    if not webpage_check(session,url):
        w = Webpage(url)
        w.url = url
        session.add(w)


#########################################################################################

def run_once():
    session = Session()
    print "Initial reset"
    my_result = session.query(TrackResource).filter(TrackResource.tracker_id > 0)
    for my_row in my_result:
        session.delete(my_row)
        
    session.query(Task).filter(Task.id > 0).delete()
    session.query(TrackerChange).filter(TrackerChange.tracker_id > 0).delete()
    
    session.query(Tracker).filter(Tracker.id > 0).delete()
    
    session.query(TrackerGroup).filter(TrackerGroup.id > 0).delete()
    session.query(User).filter(User.id > 0).delete()
    
    my_result = session.query(WebpageVersion)
    for my_row in my_result:
        session.delete(my_row)
    
    
    my_result = session.query(Registration)
    for my_row in my_result:
        session.delete(my_row)
    
    my_result = session.query(Webpage)
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
            


    def test_tracker_any_with_group(self):
        test_name("Tracker any with group")
        t = TrackerGroup()
        group_id = create_user_and_tracker_group (self.session,t)
        
        my_service = TrackerService
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = test_name()
        t.url = generate_url()
        TrackerService(my_service).insert(t)
        self.session.flush()
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = test_name()
        t.url = generate_url()
        TrackerService(my_service).insert(t)
        
        self.assertTrue(TrackerService(my_service).any_with_group(group_id))
        
        self.assertTrue(not(TrackerService(my_service).any_with_group(group_id + 1)))
                       
        
    def test_tracker_change_group(self):
        test_name("Tracker group change")
        g = TrackerGroup()
        group_id_1 = create_user_and_tracker_group (self.session,g)
        t = Tracker()
        t.tracker_group_id = group_id_1
        t.name = test_name()
        t.url = generate_url()
        my_service = TrackerService
        TrackerService(my_service).insert(t)
        self.session.flush()
        my_id = t.id
        g = TrackerGroup()
        group_id_2 = create_user_and_tracker_group (self.session,g)
        t.tracker_group_id = group_id_2
        TrackerService(my_service).update(my_id,t)
        
        self.assertTrue(TrackerService(my_service).any_with_group(group_id_2))
        
        self.assertTrue(not(TrackerService(my_service).any_with_group(group_id_1)))
        
        
        

    def test_tracker_get_all_by_group(self):
        test_name ("Tracker get all by group")
        
# Create tracker group
        u = User()
        user_id = create_user(self.session,u)
        t = TrackerGroup()    
        t.user_id = user_id    
        group_id = create_tracker_group (self.session,t)
# First tracker
        my_service = TrackerService
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = test_name()
        t.url = generate_url()
        TrackerService(my_service).insert(t)
        self.session.flush()
# Second tracker
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = test_name()
        t.url = generate_url()
        TrackerService(my_service).insert(t)
# 2nd Group
        t = TrackerGroup()
        t.user_id = user_id
        t.name = test_name()
        group_id = create_tracker_group (self.session,t)
# 3rd tracker     
        my_service = TrackerService
        t = Tracker()
        t.tracker_group_id = group_id
        name_3 = test_name()
        t.name = name_3
        t.url = generate_url()
        TrackerService(my_service).insert(t)
        self.session.flush()
        t = Tracker()
# 4th tracker
        t.tracker_group_id = group_id
        name_4 = test_name()
        t.name = name_4

        t.url = generate_url()
        TrackerService(my_service).insert(t)
        
        g = TrackerGroup()
        g.id = group_id
# Retrieve, ensure only last group's trackers retrieved.
        my_result = TrackerService(my_service).get_all_by_group(g)
        self.assertEqual (name_3, my_result[0].name)
        self.assertEqual (name_4, my_result[1].name)
# and only two.
        my_count = 0
    # Messy - cannot find attribute for number of rows!
        for my_row in my_result:
            my_count = my_count + 1
        self.assertEqual (my_count,2)
    

    def test_tracker_get_all_by_user(self):
        test_name ("Tracker get all by user")

        u = User()
        user_id = create_user (self.session,u)
        
        name_1 = test_name()
        name_2 = test_name()
        name_3 = test_name()
        name_4 = test_name()
        
        t = TrackerGroup()
                       
        t.user_id = user_id
        group_id = create_tracker_group (self.session,t)
              
        
        my_service = TrackerService
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_1
        t.url = generate_url()
        TrackerService(my_service).insert(t)
        self.session.flush()
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_2
        t.url = generate_url()
        TrackerService(my_service).insert(t)
        
        t = TrackerGroup()
                       
        t.user_id = user_id
        group_id = create_tracker_group (self.session,t)
                
        my_service = TrackerService
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_3
        t.url = generate_url()
        TrackerService(my_service).insert(t)
        self.session.flush()
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_4
        t.url = generate_url()
        TrackerService(my_service).insert(t)
       
        
        u=User()
        u.id = user_id
        
        my_result = TrackerService(my_service).get_all_by_user(u)
        self.assertEqual (name_1, my_result[0].name)
        self.assertEqual (name_2, my_result[1].name)
        self.assertEqual (name_3, my_result[2].name)
        self.assertEqual (name_4, my_result[3].name)
        
        my_count = 0
    # Messy - cannot find attribute for number of rows!
        for my_row in my_result:
            my_count = my_count + 1
        self.assertEqual (my_count,4)
    
     
    def test_tracker_delete(self): 
        test_name ("Tracker delete")
        u = User()
        my_id = create_user (self.session,u)
        t = TrackerGroup()
        t.user_id = my_id
        t.name = test_name()
        group_id = create_user_and_tracker_group (self.session,t)
        
        t=Tracker()
        t.tracker_group_id = group_id
        t.name = test_name()
        my_url = generate_url()
        t.url = my_url
        my_service = TrackerService
        TrackerService(my_service).insert(t)
        self.session.flush()
        
        wv = WebpageVersion(my_url)
        wv.url = my_url
        wv.content = "Content"
        wv.digest = "Digest"
        self.session.add(wv)
        self.session.flush 
        
        tc = TrackerChange()
        tc.tracker_id = t.id
        tc.webpage_version_id = wv.id
        tc.content = "Content"
        tc.current_css_selector = "CSS Selector"
        tc.digest = "Digest"
        tc.start_index = 123
        self.session.add(tc)

        tr = TrackResource()
        tr.tracker_id = t.id
        self.session.add(tr)

        
        my_service = TrackerService
        TrackerService(my_service).delete(t)
        my_result =  TrackerService(my_service).any_with_group(group_id)
        self.assertTrue(not(my_result))
   
    def test_tracker_insert(self):
        test_name ("Tracker Insert")
        t = TrackerGroup()
        group_id = create_user_and_tracker_group (self.session,t)
        t=Tracker()
        t.tracker_group_id = group_id
        my_name = test_name()
        t.name = my_name
        my_url = generate_url()
        t.url = my_url
        my_service = TrackerService
        TrackerService(my_service).insert(t)
        self.session.flush()
        tracker_id = t.id
    # Check webpage was created as well
        self.assertTrue(webpage_check(self.session,my_url))
    
    # Use 'get all by group' to test.
        g=TrackerGroup()
        g.id = group_id
        my_result = TrackerService(my_service).get_all_by_group(g)
        self.assertEqual (my_name, my_result[0].name)
    # Get tracjer resource
        my_result = self.session.query(TrackResource).filter(TrackResource.tracker_id == tracker_id)
        my_count = 0
        for my_row in my_result:
            my_tr = my_row.id
            my_count = my_count + 1
        
        self.assertEqual(my_count,1)
    
        my_count = self.session.query(Task).filter(Task.id == my_tr).count()
        self.assertEqual(my_count,1)
        
        
    
    def test_tracker_update(self): 
        test_name("Tracker Update")
        t = TrackerGroup()
        group_id = create_user_and_tracker_group (self.session,t)
        t=Tracker()
        t.tracker_group_id = group_id
        t.name = test_name()
        t.url = generate_url()
        my_service = TrackerService
        TrackerService(my_service).insert(t)
        self.session.flush()
        my_id = t.id
        my_name = test_name()
        t.name = my_name
        TrackerService(my_service).update(my_id,t)
        my_t =  TrackerService(my_service).get(my_id)
        self.assertEqual (my_name, my_t.name)
        self.assertEqual (my_id, my_t.id)
   

run_once()    
    
if __name__ == '__main__':
    unittest.main()