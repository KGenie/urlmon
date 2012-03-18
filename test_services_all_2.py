'''
Unit Test for Services.

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Intermediate service layer retained temporarily for the setUp method.

Be warned: produces many rows of data! 

'''

import env

from database.sqlalch import Session

 
from models.registration import Registration
from models.user import User
from models.tracker import Tracker
from models.tracker_group import TrackerGroup
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

def create_tracker_group (session,t):
# Needed for testing in several places.
    my_service = TrackerGroupService
    TrackerGroupService(my_service).insert(t)
    session.flush();
    return t.id

def create_user (session,u,randomly=None):
# Needed for testing in several places.
    my_service = UserService
    
    if randomly:
        my_time = str(time())
        u.email = my_time + "@email.com"
        u.first_name = my_time + ".first"
        u.last_name = my_time + ".last"
    
    UserService(my_service).insert(u)
    session.flush();
    return u.id
            

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
        

    
class testing(unittest.TestCase):

    def setUp(self):
        # Refresh the time and use this for variable creation.
        # Makes for messy DB but cannot sort until delete() issue solved!

        self.session = Session()
                
        self.my_time = str(time())
               
        
        self.email = "test" + self.my_time + "@polardog.co.uk"
        self.email2 = "mod" + self.my_time + "@polardog.co.uk"
        self.email3 = "base" + self.my_time + "@polardog.co.uk"
        self.email4 = "old" + self.my_time + "@polardog.co.uk"
        
        self.url = "http://www.polardog.co.uk/" + self.my_time
        
        self.reg_id = "abcd" + self.my_time
        self.tracker_group_comment = "Tracker comment"
        self.tracker_group_name = "Polar tracker"
        self.tracker_group_name = "Tropical tracker"
    
        # Create a User record to facilitate the Tracker_Group test.
        
        rowdata = service_data
        my_service = services_handler()
        rowdata.email = self.email3
        rowdata.password = "test"
        rowdata.first_name = "Lord"
        rowdata.last_name = "Ellis"
        
        self.user_id = my_service.user_insert(self.session,rowdata)
        
        
               
    def tearDown(self):
        self.session.commit()      
           
    def test_registration_insert(self):
        
        my_service = RegistrationService
        my_reg = Registration()
        my_reg.email = self.email3
        my_reg.reg_id = self.reg_id
        my_result = RegistrationService(my_service).insert(my_reg)
        self.session.flush()
        my_id = my_reg.reg_id
        self.assertEqual(self.reg_id,my_reg.reg_id)
               
    def test_registration_request(self):
    # Test unworkable because of project structure. Fudged to fai.
        my_id = 0
#       my_id = my_service.registration_request(self.session,rowdata)
        self.assertTrue(my_id)

    def test_tracker_get_all_by_user(self):
        u = User()
        user_id = create_user (self.session,u,1)
        
        name_1 = "gabu_1"
        name_2 = "gabu_2"
        name_3 = "gabu_3"
        name_4 = "gabu_4"
        
        
        t = TrackerGroup()
                       
        t.user_id = user_id
        t.name = "Test tracker get all by user 1"
        group_id = create_tracker_group (self.session,t)
                
        
        my_service = TrackerService
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_1
        t.url = "tracker_by_user.com"
        TrackerService(my_service).insert(t)
        self.session.flush()
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_2
        t.url = "tracker_by_user.com"
        TrackerService(my_service).insert(t)
        
        t = TrackerGroup()
                       
        t.user_id = user_id
        t.name = "Test tracker get all by user 2"
        group_id = create_tracker_group (self.session,t)
                
        
        my_service = TrackerService
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_3
        t.url = "tracker_by_user.com"
        TrackerService(my_service).insert(t)
        self.session.flush()
        t = Tracker()
        t.tracker_group_id = group_id
        t.name = name_4
        t.url = "tracker_by_user.com"
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
        
        
    def test_tracker_group_get_all_by_user(self):
        u = User()
        my_id = create_user (self.session,u,1)
        name_1 = "Name 1"
        name_2 = "Name 2"
        
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
    # Retrieve main user email.
        my_service = UserService
        my_row = UserService(my_service).get(self.user_id)
        my_email = my_row.email
    
    # Now create the group. Use the user email as the comment.
        t = TrackerGroup()
        t.user_id = self.user_id
        t.comment = my_email
        t.name = self.tracker_group_name
        my_service = TrackerGroupService
        TrackerGroupService(my_service).insert(t)
        self.session.flush()
        tracker_group_id = t.id
        print_number ("TGI", tracker_group_id)
        
    # Now retrieve the row and see if comment matches the user email.l
        
        my_result = TrackerGroupService(my_service).get(tracker_group_id)
        my_comment = my_result.comment
        self.assertEqual (my_email, my_comment)
   
    def test_tracker_insert(self):
        u = User()
        my_id = create_user (self.session,u,1)
        name_1 = "Trackers"
        t = TrackerGroup()
        t.user_id = my_id
        t.name = name_1
        group_id = create_tracker_group (self.session,t)
        
        t=Tracker()
        t.tracker_group_id = group_id
        my_name = "Tracker " + self.my_time
        my_url = self.my_time + "tracker.test"
        t.name = my_name
        t.url = my_url     
        my_service = TrackerService
        TrackerService(my_service).insert(t)
    # Check webpage was created as well
        self.assertTrue(webpage_check(self.session,my_url))
    
    # Use 'get all by group' to test.
        g=TrackerGroup()
        g.id = group_id
        my_result = TrackerService(my_service).get_all_by_group(g)
        self.assertEqual (my_name, my_result[0].name)
        
        
    def test_user_authenticate(self):
    # Test unworkable because of project structure. Fudged to fai.
        my_id = 0
#       my_id = my_service.registration_request(self.session,rowdata)
        self.assertTrue(my_id)
        
    
        
    
    def test_user_exists_fake(self):
        
        my_service = UserService 
        my_email = "poppycock"
        my_ok = UserService(my_service).exists(my_email)
        self.assertTrue(not(my_ok))
        
    def test_user_exists(self):
        
        my_service = UserService 
        my_email = self.email3
        my_ok = UserService(my_service).exists(my_email)
        self.assertTrue(my_ok)
    
    def test_user_insert(self):
        
        my_service = UserService
        u = User()
        u.email = self.email
        u.password = "test"
        u.first_name = "Lord"
        u.last_name = "Ellis"
        UserService(my_service).insert(u)
        self.session.flush();
        self.assertTrue(u.id)
        print_number ("User",u.id)
    
        
    def test_user_update(self):
    # Messy! Need to create user before update.
        u = User()
        u.email = self.email4
        u.password = "test"
        u.first_name = "Lord"
        u.last_name = "Ellis"
        this_id = create_user(self.session,u)
        
        print_number ("Test user update",this_id)
        
        my_service = UserService
        my_email = self.email2
                
        u.email = my_email
        
        my_service = UserService
        my_result = UserService(my_service).update(this_id, u)
        my_row = UserService(my_service).get(this_id)
        self.assertEqual(my_email,my_row.email)
        
    def test_webpage_get(self):
        my_url = "http://www.test_page.abc.com"
        webpage_create (self.session,my_url)
        my_ok = webpage_check(self.session,my_url)
        self.assertTrue (my_ok)
        
    
if __name__ == '__main__':
    unittest.main()


    