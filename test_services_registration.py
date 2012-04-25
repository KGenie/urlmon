'''
Unit Test for Registration

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Be warned: produces many rows of data! 

'''
import env

from database.sqlalch import Session
 
from models.registration import Registration
from models.user import User

from services.registration import RegistrationService

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
def create_registration(session,arg_email=None):
    
    r = Registration()

    u = User()
    
    if not arg_email:
        arg_email = generate_email()
    
    u.email = arg_email
    
    session.query(User).filter(User.email == arg_email).delete()
    
    u.first_name = "First"
    u.last_name = test_name();
        
    r.email = arg_email
    r.user = u
    my_id = test_prefix("1234")
    r.reg_id = my_id
    session.add(r)
    session.flush()
    return r.reg_id
        
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

def test_prefix(my_prefix):
    return my_prefix + "_" + str(test_next())



#########################################################################################

def run_once():
    session = Session()
    
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
        except:
            print test_name() + " commit failed" 
            self.assertTrue(0)
           
    def test_activate_user(self):
        test_name("Activate User");
        my_email = generate_email()
        reg_id = create_registration (self.session, my_email)
        my_service = RegistrationService
        RegistrationService(my_service).activate_user(reg_id)
        q = self.session.query(User).filter(User.email == my_email)
        self.assertEqual(1,q.count())
        
    def test_pending(self):
        test_name("Pending");
        my_email = generate_email()
        reg_id = create_registration (self.session, my_email)
        my_email = generate_email()
        reg_id = create_registration (self.session, my_email)
        my_service = RegistrationService
        pr = RegistrationService(my_service).pending(my_email)
        self.assertTrue(pr)
        my_email = generate_email()
        pr = RegistrationService(my_service).pending(my_email)
        self.assertTrue(not(pr))
               
    def test_registration_request(self):
        test_name("Registration Request");
        u = User()
        u.email = test_prefix("kg") + "@a222.biz"
        my_service = RegistrationService
        my_id = RegistrationService(my_service).request_registration(u)
        self.assertTrue(my_id)
        print "Check email to %s for results" % u.email

           

run_once()    
    
if __name__ == '__main__':
    unittest.main()