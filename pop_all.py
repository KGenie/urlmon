'''
Created on Feb 20, 2012

@author: bernard
'''

import env

from database.sqlalch import Session
from time import time
from tests.pop_insert import pop_insert


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
# Bug, skip for now.
#    my_insert.registration_insert(session, user, email)
    
# Create a user (fudge uniqueness using timestamp)
 
    email = my_time + "@a222.biz"
    user_id = my_insert.user_insert(session,email,"Andy","Ellis","secret")    
    print "User " + str(user_id) + " created"
      

# Use time to generate unique tracker name
    group_name = "Group name " + my_time    
    
    print group_name
    
# Create tracker group, retrieve group id
    
    group_id = my_insert.tracker_group_insert (session, group_name,user_id,"New group test")
   
    print "Tracker group " + str(group_id) + " created"
         
# With built in defaults.
    my_insert.tracker_insert(session,"Heathfield","http://www.heathfield-ecology.org.uk/home.php",group_id)
    my_insert.tracker_insert(session,"A222 - 1","HTTP://www.a222.net/home.php",group_id)
# Apply customer defaults for future inserts.
    my_insert.tracker_default ("header",600)
# With custom defaults.
    my_insert.tracker_insert(session,"Dragon","HTTP://www.electricvandandcar.co.uk",group_id,"Make a comment")
# No defaults
    my_insert.tracker_insert(session,"A222 - 2","HTTP://www.a222.net/home.php",group_id, "A comment","body",12345)
# With custom defaults again.
    my_insert.tracker_insert(session,"Banana Leaf","http://www.thebananaleaf.com",group_id)

    session.commit()
   
if __name__ == '__main__':
    populate()


