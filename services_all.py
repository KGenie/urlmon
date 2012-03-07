
import env

from database.sqlalch import Session
from models.user import User    
from tests.services_handler import services_handler, service_data
from time import time

def print_number (my_text,my_number):
        if my_number:
            try:
                my_show = str(my_number)
            except:
                my_show = "None!"
        else:
            my_show = "None!"
        print my_text + ": " + my_show
    

def services_run():
#    Utilises the services_handler class ee
#    SQL sessions are controlled from within this script.
     
    session = Session()
     
# instantiate the insert code
    my_service = services_handler()
    my_time = str(time())
    
    #   my_service.registration_insert(rowdata)
    reg_id = "abcd"
   
    email = "test@polardog.co.uk"
    
    
    
    
    url = "http://www.someweb.com/" + my_time
            
    rowdata = service_data
    rowdata.email = email
    rowdata.password = "test"
    rowdata.first_name = "Lord"
    rowdata.last_name = "Ellis"
    my_ok = my_service.registration_insert(rowdata)
    
    
# Delete if exists.
    my_id = my_service.user_retrieve_id(session,rowdata)
    if my_id:
        print_number ("User already exists as", my_id)
        rowdata.id = my_id
        my_ok = my_service.user_delete(session,rowdata)
     
    
    my_service.user_insert (session,rowdata)
  
# Check user exists (fake user)  
    
    rowdata.email = "poppycock"
    user_id = my_service.user_exists(session,rowdata)
    print_number ("Fake user",user_id)
    
    rowdata.email = email
    user_id = my_service.user_exists(session,rowdata)
    print_number ("True user", user_id)
    
    rowdata.last_name = "Altered name" + my_time
    rowdata.id = user_id
    my_ok = my_service.user_update (session, rowdata)
    
    rowdata = service_data
    rowdata.id = user_id
    my_result = my_service.user_get (session, rowdata)
    
    print "Retrieved user:"
    print my_result.email
    print my_result.first_name
    print my_result.last_name
    
    print "All users"
    my_cursor = my_service.user_get_all (session,rowdata)
    for my_row in my_cursor:
        my_show = str(my_row.id) + " " + my_row.email
        print my_show
    
    # Authenticate user (pass)

    my_result = my_service.user_get (session, rowdata)

    my_ok = my_service.user_authenticate(session,rowdata)
    try:
        my_id = my_ok.id
    except:
        my_id = None
    print_number ("User authenticate (good)", my_id)
    
# Authenticate user (fail)
   
    rowdata.password = "poppycock"
    my_ok = my_service.user_authenticate(session,rowdata)
    try:
        my_id = my_ok.id
    except:
        my_id = None
    print_number ("User authenticate (bad)", my_id)

# Create a tracker group    
   
    rowdata = service_data
    rowdata.user_id = user_id
    rowdata.name = "Tracker Group A"
    rowdata.comment = "Comment 1"
    
# Retrieve group and delete if exists.

    my_id = my_service.tracker_group_retrieve_id(session,service_data)
    
    if my_id:
        rowdata.id = my_id
        print_number ("Existing group", my_id)
        my_ok = my_service.tracker_group_delete(session,rowdata)
    
    tracker_group_id = my_service.tracker_group_insert(session,rowdata) 
    print_number ("Group",tracker_group_id)
    
    rowdata.id = tracker_group_id
    print_number ("Deleting Group",tracker_group_id)
    my_ok = my_service.tracker_group_delete(session,rowdata)
    rowdata.name = "Tracker Group B"
    
    tracker_group_id = my_service.tracker_group_insert(session,rowdata)
    print_number ("Another Group",tracker_group_id)
    first_group = tracker_group_id
    
    rowdata.name = "Tracker Group C"
    tracker_group_id = my_service.tracker_group_insert(session,rowdata)
    print_number ("Yet Another Group",tracker_group_id)
    
    rowdata = service_data
    rowdata.id = tracker_group_id
    rowdata.comment = "Comment " + my_time
    my_ok = my_service.tracker_group_update(session,rowdata)
    
    print_number ("All tracker groups for user", user_id)
    
    rowdata.user_id = user_id
    my_rows = my_service.tracker_group_get_all_by_user(session,rowdata)
    for my_row in my_rows:
        my_show = str(my_row.id) + " " + my_row.name
        print my_show
    
# Create trackers

    rowdata = service_data
    rowdata.tracker_group_id = first_group
    rowdata.url = "http://www.polardog.co.uk"
    rowdata.name = "DOG"
    tracker_id = my_service.tracker_insert(session,rowdata)
    
    rowdata = service_data
    rowdata.tracker_group_id = tracker_group_id
    rowdata.url = "http://www.a222.org.uk"
    rowdata.name = "org.uk"
    tracker_id = my_service.tracker_insert(session,rowdata)


    rowdata = service_data
    rowdata.tracker_group_id = tracker_group_id
    rowdata.url = "http://www.a222.net"
    rowdata.name = "A222"
    tracker_id = my_service.tracker_insert(session,rowdata)
    
    rowdata = service_data
    rowdata.tracker_group_id = tracker_group_id
    rowdata.url = "http://www.a222.org.uk"
    rowdata.name = "org.uk"
    tracker_id = my_service.tracker_insert(session,rowdata)

### Bug fix 
    tracker_id = 3

    print_number ("Tracker", tracker_id)

# Change the name
    
    rowdata = service_data
    rowdata.name = "co.uk"
    rowdata.id = tracker_id
    
    print rowdata.url
    
    tracker_id = my_service.tracker_update(session,rowdata)
    
    rowdata.tracker_group_id = tracker_group_id
    my_id = my_service.tracker_any_with_group(session,rowdata)
    print_number ("With group", my_id)
    
    print_number ("All trackers for user", user_id)
    rowdata.user_id = user_id
    my_rows = my_service.tracker_get_all_by_user(session,rowdata)
    for my_row in my_rows:
        my_show = str(my_row.id) + " " + my_row.url
        print my_show
         
    print_number ("All trackers for group", tracker_group_id)
    rowdata.tracker_group_id = tracker_group_id
    my_rows = my_service.tracker_get_all_by_group(session,rowdata)
    for my_row in my_rows:
        my_show = str(my_row.id) + " " + my_row.url
        print my_show
         
  
  
    session.commit()
if __name__ == '__main__':
    services_run()
