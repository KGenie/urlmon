'''
Unit Test for Services.

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Under development, intermediate test layer service_handler being progessively removed.

Be warned: produces many rows of data! 

'''

import env

from database.sqlalch import Session

from models.registration import Registration
from models.user import User
from models.tracker import Tracker
from models.tracker_group import TrackerGroup

from services.registration import RegistrationService
from services.tracker import TrackerService
from services.tracker_group import TrackerGroupService
from services.user import UserService

from tests.services_handler import services_handler, service_data

from sqlalchemy import and_
from sqlalchemy import text

from time import time

import unittest

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

    
class testing(unittest.TestCase):

    def setUp(self):
        # Refresh the time and use this for variable creation.
        # Makes for messy DB but cannot sort until delete() issue solved!

        self.session = Session()
                
        self.my_time = str(time())
               
        
        self.email = "test" + self.my_time + "@polardog.co.uk"
        self.email2 = "mod" + self.my_time + "@polardog.co.uk"
        self.email3 = "base" + self.my_time + "@polardog.co.uk"
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
    # Test is failing. Left with original test handler for now.
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = "x_" + self.email
        rowdata.password = "test"
        rowdata.first_name = "Lord"
        rowdata.last_name = "Ellis"
        my_id = 0
#       my_id = my_service.registration_request(self.session,rowdata)
        self.assertTrue(my_id)
        

            
        
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
        
    def test_user_update(self):
        
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = self.email2
        rowdata.id = self.user_id
        my_service.user_update(self.session,rowdata)
        my_id = my_service.user_exists(self.session,rowdata)
        self.assertTrue(my_id)

    
if __name__ == '__main__':
    unittest.main()


    