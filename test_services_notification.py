'''
Created on Mar 31, 2012

@author: bernard
'''

'''
Unit Test for Notifications

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

from services.notification import NotificationService
from services.tracker import TrackerService
from services.tracker_group import TrackerGroupService
from services.user import UserService
from services.webpage import WebpageService

from sqlalchemy import and_
from sqlalchemy import text

from time import time

import unittest

#########################################################################################


def create_tracker(session, arg_t, arg_object=None):
    t = Tracker()
    t.tracker_group_id = arg_t.tracker_group_id
    try:
        t.css_selector = arg_t.css_selector
    except:
        pass
    
    try:
        t.name = arg_t.name
    except:
        pass
    
    try:
        t.url = arg_t.url
    except:
        pass
    
    try:
        t.user_id = arg_t.user_id
    except:
        pass
        
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
        
    if not t.css_selector:
        t.css_selector = test_prefix("css")
        
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


def create_tracker_group (session, t, return_object=None):
       
# Needed for testing in several places.
    my_service = TrackerGroupService
    if not (t.name):
        t.name = test_name()
    TrackerGroupService(my_service).insert(t)
    session.flush();
    if return_object:
        return t
    else:
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
    
    print wv.url
    print wv.content
    print wv.digest
     
    session.add(wv)
    session.flush()
    return wv.id    

def generate_email():
    return test_name_lc() + "@kgenie.com"

def generate_url():
    return "http://www.kgenie.com/" + test_name_lc()

def mail_args():
    null = 0
    
mail_args.sender = "kgfrom@a222.biz"
mail_args.to = "kgto@a222.biz"
mail_args.template_name = "tracker_not_found"

 
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
        
    session.query(TrackerChange).filter(TrackerChange.id > 0).delete()
    session.query(Task).filter(Task.id > 0).delete()
    session.query(Tracker).filter(Tracker.id > 0).delete()
    
    
    
    session.query(TrackerGroup).filter(TrackerGroup.id > 0).delete()
    
    my_result = session.query(WebpageVersion)
    for my_row in my_result:
        session.delete(my_row)
    
    my_result = session.query(Webpage)
    for my_row in my_result:
        session.delete(my_row)
    
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



    def test_get_tracker_data(self):
        test_name("Get Tracker Data")

        u = User()
        my_email = generate_email()
        u.email = my_email
        my_user_id = create_user(self.session,u)
        tg = TrackerGroup()
        tg.user_id = my_user_id
        tracker_group_id = create_tracker_group(self.session,tg)
        
        t = Tracker()
        my_css_selector = test_prefix("css")
        t.css_selector = my_css_selector
        my_url = generate_url()
        t.url = my_url
        t.tracker_group_id = tracker_group_id
        tracker_id = create_tracker(self.session,t)
        
        my_service =  NotificationService
        td = NotificationService(my_service).get_tracker_data(tracker_id)
        
        self.assertEqual(td.css_selector,my_css_selector)
        self.assertEqual(td.email, my_email)
        self.assertEqual(td.url,my_url)
        self.assertEqual(td.user_id,my_user_id)

    def test_notify_no_tracker(self):
        test_name("Notify No tracker")

        u = User()
        my_email = test_prefix("kg") + "@a222.biz"
        u.email = my_email
        my_user_id = create_user(self.session,u)
        tg = TrackerGroup()
        tg.user_id = my_user_id
        tracker_group_id = create_tracker_group(self.session,tg)
       
        t = Tracker()
        my_css_selector = test_prefix("css")
        t.css_selector = my_css_selector
        my_url = generate_url()
        t.url = my_url
        t.tracker_group_id = tracker_group_id
        tracker_id = create_tracker(self.session,t)

        my_service =  NotificationService
        td = NotificationService(my_service).notify_no_tracker(tracker_id)

        print "Email values:-"
        print my_email
        print my_url
        print "(end)"

        self.assertTrue(td)

    def test_notify_tracker_updated(self):
        test_name("Notify Tracker updated")

        u = User()
        my_email = test_prefix("kg") + "@a222.biz"
        u.email = my_email
        my_user_id = create_user(self.session,u)
        tg = TrackerGroup()
        tg.user_id = my_user_id
        tracker_group_id = create_tracker_group(self.session,tg)
       
        t = Tracker()
        my_css_selector = test_prefix("css")
        t.css_selector = my_css_selector
        my_url = generate_url()
        t.url = my_url
        t.tracker_group_id = tracker_group_id
        tracker_id = create_tracker(self.session,t)

        old_content = test_prefix("Old")
        new_content = test_prefix("New")
        my_service =  NotificationService
        td = NotificationService(my_service).notify_tracker_updated(tracker_id, old_content, new_content)

        print "Email values:-"
        print my_email
        print my_url
        print old_content
        print new_content
        print "(end)"

        self.assertTrue(td)    

    def test_request_registration(self):
        test_name ("Request Registration")
        u = User()
        u.email = test_prefix ("kg") + "@a222.biz"
        reg = Registration(u)
        reg.email = u.email
        self.session.add(reg)
        reg_id = reg.reg_id
        test_url = "http://fake.kgenie.com"
        my_service =  NotificationService
        my_ok = NotificationService(my_service).request_registration (reg_id, test_url)
        self.assertTrue(my_ok)
        print "Check for email to %s" % u.email

    def test_send_mail(self):
    # Will require manual checking of email content
        test_name ("Send mail")
        my_to = mail_args.to
        my_from = mail_args.sender
                        
        my_subject = "Simple mail: " + test_name()
        my_content = "Content: " + test_name()
        my_service =  NotificationService
        td = NotificationService(my_service).send_mail (my_to, my_subject, my_content, None, None, my_from)
        
        print "Email values:-"
        print my_to
        print my_subject
        print my_content
        print my_from
        print "(end)"
        
        
                
        self.assertTrue(td)
        
    def test_send_template_mail(self):
    # Will require manual checking of email content
        test_name ("Send template mail")
        my_to = mail_args.to

        my_subject = "Template mail: " + test_name()
        my_template = mail_args.template_name
        my_url = generate_url()
        my_context = { 'url': my_url }
        my_service =  NotificationService
        td = NotificationService(my_service).send_template_mail (my_to, my_subject, my_template, my_context)
        
        print "Email values:-"
        print my_to
        print my_subject
        print my_url
        print "(end)"
               
        self.assertTrue(td)
        
    
            
run_once()    
    
if __name__ == '__main__':
    unittest.main()