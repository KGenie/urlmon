'''
20-02-2012    Created

Test handler (though parts might have permanent uses) for the Services layer.

Each method expects the same arguments:

session:           A current sqlalchemy session.
service_data:      Collection of row data. Simplest technique to (re-)initialise is to instantiate from 'service_data' (from this module)   

Returned data:

is either datum, collection or array.

datum return are named *_id. Most are numeric, not all. This will generally be the ID created when adding a record or a 0/1 fail/success.
 
collection occurs where a row of data is returned. Named my_row. Typical in _get methods.

array occurs where more than one row could be returned. Named my_result. Typical in _get_all methods.

A zero, null or false result indicates that the operation has failed.

NOTES:

DELETE methods have been fudged because of a general problem with session.delete()
As a workround, these methods change the unique key to something meaningless thus 
effectively deleting for test purposes. 

Method 'tracker_retrieve_id' is failing with an unexplained SQL error. Calls have been bypassed for the moment.

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
from sqlalchemy import and_
from time import time
 

def service_data():
    null = 0;

class services_handler:
    
    def registration_insert (self,session,service_data):
        my_service = RegistrationService
        my_email = service_data.email
        my_reg = Registration()
        my_reg.email = my_email
        my_reg.reg_id = service_data.reg_id
        my_result = RegistrationService(my_service).insert(my_reg)
        my_id = self.registration_retrieve(session, service_data)
        return my_id
        
    def registration_request (self,session,service_data):
        my_service = RegistrationService
        my_email = service_data.email
        my_user = User()
        my_user.email = my_email
        my_result = RegistrationService(my_service).request_registration(my_user)
        my_id = self.registration_retrieve(session, service_data)
        return my_id
         
    def registration_retrieve(self,session,service_data):
                   
        my_email = service_data.email
        
                        
        my_result = session.query(Registration).filter(Registration.email==my_email).first()
        try:
            reg_id = my_result.reg_id
        except:
            reg_id = 0
        return reg_id

    def tracker_any_with_group (self,session, service_data):
        my_service = TrackerService

        my_id = service_data.tracker_group_id
        
        my_result = TrackerService(my_service).any_with_group(my_id) 
        try:
            id = my_result.id
        except:
            id = 0
        return id
    
    def tracker_get_all_by_group (self,session, service_data):
        my_service = TrackerService
        t = TrackerGroup
        my_id = service_data.tracker_group_id
        t.id = my_id
        my_result = TrackerService(my_service).get_all_by_group(t)
        return my_result
    
    def tracker_get_all_by_user (self,session, service_data):
        my_service = TrackerService
        t = User()
        t.id = service_data.user_id
        my_result = TrackerService(my_service).get_all_by_user(t)
        return my_result
    
    def tracker_group_get_all_by_user (self,session, service_data):
        my_service = TrackerGroupService
        t = User()
        t.id = service_data.user_id
        my_result = TrackerGroupService(my_service).get_all_by_user(t)
        return my_result
        

    def tracker_group_delete (self,session,service_data):       
        my_service = TrackerGroupService
        t = TrackerGroup()
        my_id = service_data.id
        t.id = my_id
#        my_ok = TrackerGroupService(my_service).delete(t)
        t.name = "zzz:" + str(time())
        my_ok = TrackerGroupService(my_service).update(my_id,t)
        return 1
    
    def tracker_group_get (self,session,service_data):       
        my_service = TrackerGroupService
        t = TrackerGroup()
        my_id = service_data.id
        my_result = TrackerGroupService(my_service).get(my_id)
        return my_result
        
    def tracker_group_insert (self,session, service_data):
        my_service = TrackerGroupService
        t = TrackerGroup()
        t.name = service_data.name
        t.user_id = service_data.user_id
        t.comment = service_data.comment
        my_ok = TrackerGroupService(my_service).insert(t)
        my_id = self.tracker_group_retrieve_id (session, service_data)
        return my_id
    
    def tracker_group_retrieve_id (self,session, service_data):
        my_service = TrackerGroupService
        t = TrackerGroup()
        t.name = service_data.name
        t.user_id = service_data.user_id
            
        my_name = t.name
        my_user = t.user_id
        
        my_result = session.query(TrackerGroup).filter(and_(TrackerGroup.name==my_name,TrackerGroup.user_id==my_user)).first()
        try:
            id = my_result.id
        except:
            id = 0
        return id
    
    def tracker_group_update (self,session, service_data):
        my_service = TrackerGroupService
        t = TrackerGroup()
        my_id = service_data.id
        t.id = my_id
        try:
            t.name = service_data.name
        except:
            pass
        try:
            t.user_id = service_data.user_id
        except:
            pass
        try:
            t.comment = service_data.comment
        except:
            pass
        my_ok = TrackerGroupService(my_service).update(my_id,t)
            
        
    def tracker_insert (self,session,service_data):
        
        tracker_service = TrackerService

        my_tracker = Tracker()
        
        my_tracker.url = service_data.url
        
        try:
            my_tracker.comment = service_data.comment
        except:
            pass
        try:
            my_tracker.css_selector = service_data.css_selector
        except:
            pass
        try:
            my_tracker.frequency = service_data.frequency
        except:
            pass
                
        my_tracker.name = service_data.name
        my_tracker.tracker_group_id = service_data.tracker_group_id
        my_result = TrackerService(tracker_service).insert(my_tracker)
        my_id = 0
#        my_id = self.tracker_retrieve_id(session, service_data)
        return my_id

    def tracker_retrieve_id (self,session, service_data):
        t = Tracker()
        
        t.url = service_data.url
        t.tracker_group_id = service_data.tracker_group_id
        
        my_url = service_data.url
        my_tracker_group_id = service_data.tracker_group_id
        
        my_result = session.query(Tracker).filter(and_(Tracker.tracker_group_id==my_tracker_group_id,Tracker.url==my_url)).first()
        try:
            id = my_result.id
        except:
            id = 0
        return id
    
    def tracker_update (self,session, service_data):
       
        tracker_service = TrackerService

        my_tracker = Tracker()
        my_id = service_data.id
        my_tracker.id = my_id
        try:
            my_tracker.url = service_data.url
        except:
            pass
        try:
            my_tracker.comment = service_data.comment
        except:
            pass
        try:
            my_tracker.css_selector = service_data.css_selector
        except:
            pass
        try:
            my_tracker.frequency = service_data.frequency
        except:
            pass
        try:        
            my_tracker.name = service_data.name
        except:
            pass
        try:        
            my_tracker.tracker_group_id = service_data.tracker_group_id
        except:
            pass
        
        my_result = TrackerService(tracker_service).update(my_id,my_tracker)
        return 1
       


    
    def user_authenticate (self,session,service_data):
       user_service = UserService
       email = service_data.email
       password = service_data.password
       my_ok = UserService(user_service).authenticate(email,password)
       if my_ok:
           user_id = my_ok.id
       else:
            user_id = 0
       return user_id
        
    def user_delete (self,session,service_data):
        my_service = UserService
        my_user = User()
        my_id = service_data.id
        
        my_user.id = my_id
                
        #my_result = UserService(my_service).delete(my_user)
        
        my_user.email = str(time()) + "@invalid.com"
        my_ok = UserService(my_user).update(my_id,my_user)
        return 1 
    
    
    def user_exists (self,session,service_data):
# See if user exists. If so, return ID
       user_service = UserService
       email = service_data.email
       user_id = 0
       my_exists = UserService(user_service).exists(email)
       if my_exists:
           return 1
       else:
           return 0
    

    def user_get (self,session,service_data):
        my_service = UserService
        my_id = service_data.id
        
        my_row = UserService(my_service).get(my_id)
        return my_row
    
    def user_get_all (self,session,service_data):
        my_service = UserService
        my_result = UserService(my_service).get_all()
        return my_result
            
    def user_insert (self,session,service_data):
        my_service = UserService
        my_user = User()
        my_user.email = service_data.email
        my_user.first_name = service_data.first_name
        my_user.last_name = service_data.last_name
        try:
            my_user.full_name = service_data.full_name
        except:
            my_user.full_name = service_data.first_name + " " + service_data.last_name
                        
        try:
            my_user.roles = service_data.roles
        except:
            my_user.roles = ""
        my_user.password = service_data.password

        my_result = UserService(my_service).insert(my_user)
        
        my_id = self.user_retrieve_id (session,service_data) 
        return my_id
        
    def user_register (self,session,service_data):
       registration_service = RegistrationService
       reg_id = service_data.reg_id
       my_result = RegistrationService(registration_service).activate_user(reg_id)
    
    def user_retrieve_id (self,session, service_data):
        
        u = User()
                          
        my_email = service_data.email
        
        my_result = session.query(User).filter(User.email==my_email).first()
        try:
            id = my_result.id
        except:
            id = 0
        return id
        
    def user_update (self,session,service_data):
        my_service = UserService
        my_user = User()
        my_id = service_data.id
       
        my_user.id = my_id
        
        try:
            my_user.email = service_data.email
       
        except:
            pass
        try:
            my_user.first_name = service_data.first_name
        except:
            pass
        try:
            my_user.last_name = service_data.last_name
        except:
            pass
        try:
            my_user.full_name = service_data.full_name
        except:
            pass
        try:
            my_user.roles = service_data.roles
        except:
            pass
        try:
            my_user.password = service_data.password
        except:
            pass

        my_result = UserService(my_service).update(my_id, my_user)
        
        return 1 
        
       
       