'''
Unit Test for Services.

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Uses an intermediate module which is 'tests.services_handler' which calls the actual service layer.

Be warned: produces many rows of data! 

'''

import env
from database.sqlalch import Session
from models.user import User    
from tests.services_handler import services_handler, service_data
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
        session = Session()
        self.user_id = my_service.user_insert(session,rowdata)
               
        
        session.commit()
        
           
    def test_registration_insert(self):
        session = Session()
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = self.email
        rowdata.reg_id = self.reg_id
        rowdata.password = "test"
        rowdata.first_name = "Lord"
        rowdata.last_name = "Ellis"
        my_id = my_service.registration_insert(session,rowdata)
        self.assertTrue(my_id)
        session.commit()
       
    def test_registration_request(self):
        session = Session()
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = "x_" + self.email
        rowdata.password = "test"
        rowdata.first_name = "Lord"
        rowdata.last_name = "Ellis"
        my_id = 0
#       my_id = my_service.registration_request(session,rowdata)
        self.assertTrue(my_id)
        session.commit()

    def test_user_insert(self):
        session = Session()
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = self.email
        rowdata.password = "test"
        rowdata.first_name = "Lord"
        rowdata.last_name = "Ellis"
        my_id = my_service.user_insert (session,rowdata)
        self.assertTrue(my_id)
        session.commit()
    
    def test_user_exists_fake(self):
        session = Session()
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = "poppycock"
        my_ok = my_service.user_exists(session,rowdata)
        self.assertTrue(not(my_ok))
        session.rollback()

    def test_user_exists(self):
        session = Session()
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = self.email3
        my_ok = my_service.user_exists(session,rowdata)
        self.assertTrue(my_ok)
        session.rollback()
        
    def test_user_update(self):
        session = Session()
        my_service = services_handler() 
        rowdata = service_data
        rowdata.email = self.email2
        rowdata.id = self.user_id
        my_service.user_update(session,rowdata)
        my_id = my_service.user_exists(session,rowdata)
        self.assertTrue(my_id)
        session.commit()
        
    def test_tracker_group_insert(self):
        session = Session()
        
        my_service = services_handler()
    
    # Retrieve User email 
        rowdata = service_data
        rowdata.id = self.user_id
        my_result = my_service.user_get(session,rowdata)
        my_email = my_result.email
    
    # Now create the group. Use the user email as the comment.
        rowdata = service_data
        rowdata.user_id = self.user_id
        rowdata.comment = my_email
        rowdata.name = self.tracker_group_name
        tracker_group_id = my_service.tracker_group_insert(session,rowdata)
        
    # Now retrieve the row and see if comment matches the user email.
        rowdata.id =  tracker_group_id
        my_result = my_service.tracker_group_get(session,rowdata)
        my_comment = my_result.comment
        self.assertEqual (my_email, my_comment)
        session.commit()
    
if __name__ == '__main__':
    unittest.main()


    