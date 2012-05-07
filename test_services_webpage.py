'''
Unit Test for Services.

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Be warned: produces many rows of data!

'''
import env

from database.sqlalch import Session
 
from models.task import Task
from models.tracker import Tracker
from models.tracker_group import TrackerGroup
from models.track_resource import TrackResource
from models.user import User
from models.webpage import Webpage


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

def generate_url(arg_plain=False):
    
    my_url = "www.kgenie.com/" + test_name_lc()
    
    if not arg_plain:
        my_url = "http://" + my_url
    
    return my_url
 
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
    null = 0
    
test_iteration.counter = 0
test_iteration.name = ""

def test_name(my_name=None):
    if my_name:
        test_iteration.name = my_name
    return test_iteration.name + "_" + str(test_next())

def test_name_lc ():
    my_name = test_name()
    my_name = my_name.lower()
    my_name = my_name.replace(" ","_")
    return my_name

def test_next():
    test_iteration.counter = test_iteration.counter + 1
    return test_iteration.counter

def test_suffix(my_suffix):
    return my_suffix + "_" + str(test_next())

def webpage_check (session,my_url):
     if session.query(Webpage).filter(Webpage._url == my_url).count() == 0:
          return False
     else:
         return True
     
def webpage_create(session,url):
    if not webpage_check(session,url):
        w = Webpage(url)
        my_service = WebpageService
        WebpageService(my_service).insert(w)
        

#########################################################################################

def run_once():
    session = Session()
    print "Initial reset"
    my_result = session.query(TrackResource).filter(TrackResource.tracker_id > 0)
    for my_row in my_result:
        session.delete(my_row)
        
    session.query(Task).filter(Task.id > 0).delete()
    session.query(Tracker).filter(Tracker.id > 0).delete()
    
    my_result = session.query(Webpage)
    for my_row in my_result:
        session.delete(my_row)
    
    session.query(TrackerGroup).filter(TrackerGroup.id > 0).delete()
           
    session.commit()
    


        
    
class testing(unittest.TestCase):

    def setUp(self):

        self.session = Session()
              
    def tearDown(self):
        try:
            self.session.commit()
        except:
            print test_name() + " commit failed"
            self.assertTrue(0)
    
    def test_webpage_case_check_r(self):
        test_name ("Case Check R")
        my_url = generate_url(-1)
        my_target = "http://" + my_url
        my_url = "HTTP://HTTPS://" + my_url
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_target))
    
    def test_webpage_case_check_s(self):
        test_name ("Case Check S")
        my_url = generate_url(-1)
        my_target = "https://" + my_url
        my_url = "HTTPS://HTTP://" + my_url
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_target))
    
    
            
    def test_webpage_get(self):
        test_name ("Webpage Get")
        my_url = generate_url()
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_url))

    def test_webpage_mangled_rr(self):
        test_name ("Mangled rr")
        my_url = generate_url(-1)
        my_target = "http://" + my_url
        my_url = "http://http://" + my_url
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_target))
    
    def test_webpage_mangled_rs(self):
        test_name ("Mangled rs")
        my_url = generate_url(-1)
        my_target = "http://" + my_url
        my_url = "http://https://" + my_url
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_target))
    
    def test_webpage_mangled_sr(self):
        test_name ("Mangled sr")
        my_url = generate_url(-1)
        my_target = "https://" + my_url
        my_url = "https://http://" + my_url
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_target))
    
    def test_webpage_mangled_ss(self):
        test_name ("Mangled ss")
        my_url = generate_url(-1)
        my_target = "https://" + my_url
        my_url = "https://https://" + my_url
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_target))
    
    
    def test_webpage_plain(self):
        test_name ("Webpage plain")
        my_url = generate_url(-1)
        webpage_create (self.session,my_url)
        my_target = "http://" + my_url
        self.assertTrue (webpage_check(self.session,my_target))
    
    def test_webpage_regular(self):
        test_name ("Webpage secure")
        my_url = generate_url()
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_url))
    
        
    def test_webpage_secure(self):
        test_name ("Webpage secure")
        my_url = generate_url(-1)
        my_url = "https://" + my_url
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_url))
    
run_once()
    
if __name__ == '__main__':
    unittest.main()