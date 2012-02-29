'''
29/02/2012    Andy

General purpose insert methods.

With the exception of the 'user_insert' which is currently experimental, this operates as follows:

pop_insert() is imported by the calling script and instantiated.
pop_data() is imported by the calling script. This is used to define the 'rowdata' argument used in the _insert methods.

config_return_result(return_result) creates a persistent parameter which dictates whether the id of a newly created row should be returned. 
Arguments are 0 = no return, 1 = return. The 'no return' setting will improve performance.
If never called then the value hardcoded in return_result is used.

tracker_default (css_selector,frequency) sets persistent default values for these tracker fields. If never called then the 
values hardcoded in  default_data {} will be used.

tracker_group_insert (session,rowdata,result_arg=None). Used here as an example, other *_insert work in the same way.
session is the current SQLALCHEMY session.
rowdata comprises the required data, it is built per the following example:
rowdata = pop_data
rowdata.user_id = user_id
rowdata.group_name = "Test group"
result_arg (optional) overrides the default return result option, as controlled by config_return_result().
Arguments: 0 = no result, 1 = return result. 
If omitted then the current default method is deployed

!! OBSERVATION: The method for returning the latest ID where there is no unique key (e.g. in Task) does work but requires review.

'''



from models.registration import Registration
from models.task import Task
from models.tracker import Tracker

from models.tracker_group import TrackerGroup

from models.user import User
from models.webpage import Webpage
from util import normalize_url
from sqlalchemy import *

def pop_data():
    null = 0

class pop_insert:

    pop_rowdata = {}
    
#define initial defaults for tracker values. These may be overriden via the tracker_default method.        
    default_data = {}
    default_data["tracker_css_selector"] = "body"
    default_data["tracker_frequency"] = 300
    
# configuration data
    return_result = 1
    
    def config_return_result (self,mode):
        if mode == 1:
            self.return_result = 1
        else:
            self.return_result = 0
        
    def pop_add (self,column,datum):
        self.pop_rowdata[column] = datum
        
    def registration_insert (self, session, user, email):
        # my_ok = self.exists_check("webpage","url",url_arg)
        r = Registration(user=user)
        r.email=user.email
        session.add(r)
    
    
    def task_insert (self,session,rowdata,result_arg=None):
        try:
            next_run = rowdata.next_run
        except:
            next_run = None
                        
        t = Task(next_run)
        session.add(t)
        if result_arg == None:
            result_arg = self.return_result
        if result_arg:            
        # Return new used ID (I don't like this, must be better way)
           session.flush()
           my_id = t.id
           return my_id
    
    
    
    def tracker_default (self,css_selector,frequency):
        self.default_data["tracker_css_selector"] = css_selector
        self.default_data["tracker_frequency"] = frequency
    
    
    def tracker_delete(self, session, rowdata):
       id = rowdata.id
       session.query(Tracker).filter(Tracker.id==id).delete()
                  
    def tracker_group_insert (self,session,rowdata,result_arg=None):
    # Insert group, return group id.
        user = rowdata.user_id
        name = rowdata.group_name
        try:
            comment = rowdata.comment
        except:
            comment=None
        
        g = TrackerGroup(name=name, user_id=user, comment=comment)
        session.add(g)
        if result_arg == None:
            result_arg = self.return_result
        if result_arg:            
            session.flush()
            my_id = g.id
            return my_id
    
    
        
    def tracker_insert(self, session, rowdata, result_arg=None):
        name = rowdata.name
        url = rowdata.url 
        tracker_group_id = rowdata.tracker_group_id
        
        try:
            comment = rowdata.comment
        except:
            comment=None

# Default selector and frequency.
        
                
        try:
            frequency = rowdata.frequency
        except:
            frequency = self.default_data["tracker_frequency"] 
        
        try:
            css_selector = rowdata.css_selector
        except:
            css_selector = self.default_data["tracker_css_frequency"] = frequency
      
        
# Make sure there is a corresponding webpage record. Create if there is none.

        my_url = normalize_url(url)
        if session.query(Webpage).filter(Webpage._url == my_url).count() == 0:
            self.webpage_insert(session, my_url)

        my_url = normalize_url(my_url)

# Create the tracker.

        t = Tracker(name=name, url=my_url,frequency=frequency, tracker_group_id=tracker_group_id,comment=comment, css_selector=css_selector)
        session.add(t)
        if result_arg == None:
            result_arg = self.return_result
        if result_arg:            
            session.flush()
            my_id = t.id
            return my_id

    def tracker_update(self, session, rowdata):
       id = rowdata.id
       ret = session.query(Tracker).filter(Tracker.id == id)
       if ret:
           for row in ret:
               try:
                   row.name=rowdata.name
               except:
                   pass

            
    def user_insert (self,session,result_arg=None):
        email = self.pop_rowdata["email"]
        first_name = self.pop_rowdata["first_name"]
        last_name = self.pop_rowdata["last_name"]
        try:
            full_name = self.pop_rowdata["full_name"]
        except:
            full_name = first_name + " " + last_name
                        
        try:
            roles = self.pop_rowdata["roles"]
        except:
            roles = ""
        password = self.pop_rowdata["password"]
              
        u = User(email=email,first_name=first_name,last_name=last_name, password=password,full_name=full_name, roles=roles)
        session.add(u)
        self.pop_rowdata = {}
        if result_arg == None:
            result_arg = self.return_result
        if  result_arg:
            # Return new user ID
#            my_query = session.query(User).filter(User.email == email).first()
#            my_id = my_query.id
            session.flush()
            my_id = u.id
            return my_id
               

    def webpage_insert (self, session, url_arg, result_arg=None):
#        my_ok = self.exists_check("webpage","url",url_arg)
        w = Webpage(url=url_arg)
        session.add(w)
        return 0
    