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
            

           
    def test_registration_insert(self):
        test_name("Registration Insert");        
        my_service = RegistrationService
        r = Registration()
        r.email = generate_email()
        r.email = "bazin.frederic@gmail.com"
        my_id = test_suffix("1234")
        r.reg_id = my_id
        RegistrationService(my_service).insert(r)
        self.session.flush()
        self.assertEqual(my_id,r.reg_id)
               
    def test_registration_request(self):
    # Unit testing not possible. This is because the Service references context data which cannot be emulated in unit-test. Accordingly test is set to fail.
        test_name("Registration Request");
        u = User()
        u.email = "kg@a222.biz"
        my_service = RegistrationService
        my_id = RegistrationService(my_service).request_registration(u)
        self.assertTrue(my_id)

    def test_reconstruct_url(self):
    # Initial test, not true unittest at this time.
        my_reg = "1234"
        my_service = RegistrationService
        my_url = RegistrationService(my_service).reconstruct_url(my_reg)
        print my_url
           

run_once()    
    
if __name__ == '__main__':
    unittest.main()