'''
Created on Feb 20, 2012

@author: bernard
'''

import env

from database.sqlalch import Session
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
    
# Create a user (in progress, mock it for now)
    user_id = 1    
        
    session = Session()
# Create tracker group, retrieve group id    
    my_tracker = my_insert.tracker_group_insert (session, "New Group",user_id,"New group test")
# Commit at this ppoint and retrieve tracker insert    
    session.commit()  
    session.refresh(my_tracker)
    group_id = my_tracker.id
    
    print "Tracker group " + str(group_id) + " created"

    session = Session()
     
# With built in defaults.
    my_insert.tracker_insert(session,"Heathfield","http://www.heathfield-ecology.org.uk/home.php",group_id)
# Apply customer defaults for future inserts.
    my_insert.tracker_default ("header",600)
# With custom defaults.
    my_insert.tracker_insert(session,"Dragon","http://www.electricvandandcar.co.uk",group_id,"Make a comment")
# No defaults
    my_insert.tracker_insert(session,"A222","http://www.a222,net/home.php",group_id, "A comment","body",12345)
# With custom defaults again.
    my_insert.tracker_insert(session,"Banana Leaf","http://www.thebananaleaf.com",group_id)

    session.commit()
   
if __name__ == '__main__':
    populate()


