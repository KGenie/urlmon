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
from models.tracker_group import TrackerGroup
from models.track_resource import TrackResource
from models.user import User
from models.webpage import Webpage


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
            
    
           
    def test_tracker_group_get_all_by_user(self):
        test_name("Test tracker group get all by user")
        u = User()
        my_id = create_user (self.session,u)
        name_1 = test_name()
        name_2 = test_name()
        
        t = TrackerGroup()
                        
        t.user_id = my_id
        t.name = name_1
        create_tracker_group (self.session,t)
        
        t = TrackerGroup()
        t.user_id = my_id
        t.name = name_2
        create_tracker_group (self.session,t)

        my_service = TrackerGroupService
        t = User()
        t.id = my_id
        my_result = TrackerGroupService(my_service).get_all_by_user(t)
        self.assertEqual (name_1, my_result[0].name)
        self.assertEqual (name_2, my_result[1].name)
        my_count = 0
    # Messy - cannot find attribute for number of rows!
        for my_row in my_result:
            my_count = my_count + 1
        self.assertEqual (my_count,2)

    def test_tracker_group_insert(self):
        test_name("Tracker Group Insert")
    # Retrieve main user email.
        u = User()
        user_id = create_user(self.session,u)
        my_service = UserService
        my_row = UserService(my_service).get(user_id)
        my_email = my_row.email
    
    # Now create the group. Use the user email as the comment.
        t = TrackerGroup()
        t.user_id = user_id
        t.comment = my_email
        t.name = test_name()
        my_service = TrackerGroupService
        TrackerGroupService(my_service).insert(t)
        self.session.flush()
        tracker_group_id = t.id
        
    # Now retrieve the row and see if comment matches the user email.l
        
        my_result = TrackerGroupService(my_service).get(tracker_group_id)
        my_comment = my_result.comment
        self.assertEqual (my_email, my_comment)
           
        
    def test_user_authenticate(self):
    # Unit testing not possible. This is because the Service references context data which cannot be emulated in unit-test. Accordingly test is set to fail.
        test_name ("User Authenticate")
    # Test unworkable because of project structure. Fudged to fai.
        my_id = 0
#       my_id = my_service.registration_request(self.session,rowdata)
        self.assertTrue(my_id,"Test not workable because of context issues")
        
    
    def test_user_exists_fake(self):
        test_name ("User Exists fake")
        my_service = UserService 
        my_email = generate_email()
        my_ok = UserService(my_service).exists(my_email)
        self.assertTrue(not(my_ok))
        
    def test_user_exists(self):
        test_name ("User Exists")
        u = User()
        my_service = UserService 
        my_email = generate_email()
        u.email = my_email
        create_user(self.session,u)
        my_ok = UserService(my_service).exists(my_email)
        self.assertTrue(my_ok)
    
    def test_user_insert(self):
        test_name ("User Insert")
        my_service = UserService
        u = User()
        my_email = generate_email()
        u.email = my_email
        u.first_name = "First"
        u.last_name = test_name()
        u.password = "password"
        UserService(my_service).insert(u)
        self.session.flush();
        my_id = u.id
        my_ok = UserService(my_service).exists(my_email)
        self.assertTrue(my_ok)
   
        
    def test_user_update(self):
        test_name ("User update")
        u = User()
        u.email = test_suffix ("any") + "@kgenie.com"
        this_id = create_user(self.session,u)
               
        my_service = UserService
        my_email = generate_email()
                
        u.email = my_email
        
        my_result = UserService(my_service).update(this_id, u)
        my_row = UserService(my_service).get(this_id)
        self.assertEqual(my_email,my_row.email)
        
    def test_webpage_get(self):
        test_name ("Webpage get")        
        my_url = generate_url()
        webpage_create (self.session,my_url)
        self.assertTrue (webpage_check(self.session,my_url))

run_once()    
    
if __name__ == '__main__':
    unittest.main()