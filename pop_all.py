'''
Created on Feb 20, 2012
@author: bernard




'''

import env
from datetime import datetime

from database.sqlalch import Session

from time import time
from tests.pop_insert import pop_insert, pop_data
    

def populate():
    '''
    Utilises the pop_insert class from module pop_insert
    SQL sessions are controlled from within this script.
    my_insert.tracker_default method may be used to set default selector and frequency for subsequent tracker inserts.
    There is no 'teardown' at this point. Existing data will need to be cleared manually    
    '''
 
# instantiate the insert code
    my_insert = pop_insert()
    
    session = Session()
    
    my_time = str(time())
    
# Create a registration

    user = "User " + my_time
    email = "register@a222.biz"

#    my_insert.registration_insert(session, user, email)

# Create user (not the standard method, some experimentation here but probably won't go down this road)
    
    my_insert.pop_add ("email",my_time + "@a222.org")
    my_insert.pop_add("first_name","Xerxes")
    my_insert.pop_add("last_name","The 4th")
    my_insert.pop_add("password","test")
    user_id = my_insert.user_insert(session)    
    print "User " + str(user_id) + " created"

# Quick insert (does not return ID)
    
    my_insert.pop_add ("email",my_time + "@a222.org.uk")
    my_insert.pop_add("first_name","Neon")
    my_insert.pop_add("last_name","is inert")
    my_insert.pop_add("password","test")
    user_id2 = my_insert.user_insert(session,0)    
    print "User " + str(user_id2) + " created"
    
# Use time to generate unique tracker name
    group_name = "Group name " + my_time    
    
    print group_name
    
    rowdata = pop_data
    rowdata.user_id = user_id
    rowdata.group_name = group_name
    
# Create tracker group, retrieve group id
    
    group_id = my_insert.tracker_group_insert (session, rowdata)
   
    print "Tracker group " + str(group_id) + " created"
         
# TRACKERS
    
    web_pages = {}
    web_pages[1] = "http://www.a222.net/home.php" 
    web_pages[2] = "http://www.a222.net/links.php"
    web_pages[3] = "http://www.a222.net/portfolio.php"

# Turn off result return:
    my_insert.config_return_result(0)

# Using built in defaults.
    rowdata = pop_data
    rowdata.tracker_group_id = group_id
    rowdata.name = "Test1"
    rowdata.url = web_pages[1]
    print my_insert.tracker_insert(session,rowdata)
# Apply custom defaults for future inserts.
    my_insert.tracker_default("header", 777)
# With custom defaults and overwrite result return
    rowdata.name = "Test2"
    rowdata.url = web_pages[2]
    print my_insert.tracker_insert(session,rowdata,1)

# Turn on result return:
    my_insert.config_return_result(1)
  
# No defaults
    rowdata.name = "Test3"
    rowdata.url = web_pages[3]
    rowdata.frequency = 123
    rowdata.css_selector = "custom"
    print my_insert.tracker_insert(session,rowdata)
# With custom defaults again but no result
    rowdata.tracker_group_id = group_id
    rowdata.name = "Test4"
    rowdata.comment = "Comment"
    rowdata.url = "http://www.a222.net/news.php"
    del (rowdata.css_selector)
    del (rowdata.frequency)
    print my_insert.tracker_insert(session,rowdata,0)
    
    
    
    
    # TASK
    
    rowdata = pop_data
    my_id = my_insert.task_insert(session,rowdata)
    print "Task " + str(my_id) + " created"
    
    # Task with current date and time.
    
    my_now = datetime.now()
    rowdata = pop_data
    rowdata.next_run = my_now
    my_id = my_insert.task_insert(session,rowdata)
    print "Task " + str(my_id) + " created"
    
    
    
    
    session.commit()
   
if __name__ == '__main__':
    populate()


