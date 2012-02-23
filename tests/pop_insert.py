from models.registration import Registration
from models.tracker import Tracker

from models.tracker_group import TrackerGroup

from models.user import User
from models.webpage import Webpage
from util import normalize_url
from sqlalchemy import *

class pop_insert:


#define initial defaults for tracker values. These may be overriden via the tracker_default method.    
    default_tracker_css_selector = "body"
    default_tracker_frequency = 300
    
    
    def registration_insert (self, session, user, email):
#        my_ok = self.exists_check("webpage","url",url_arg)
        r = Registration(user=user)
        r.email=user.email
        session.add(r)
    
    
    def tracker_default (self,css_selector,frequency):
        self.default_tracker_css_selector = css_selector
        self.default_tracker_frequency = frequency
    
    
    def tracker_group_insert (self,session,name,user,comment=None):
    # Insert group, return group id.
        
        g = TrackerGroup(name=name, user_id=user, comment=comment)
        session.add(g)
        my_query = session.query(TrackerGroup).filter(TrackerGroup.name == name).first()
        my_id = my_query.id
        return my_id
        
    def tracker_insert(self, session, name, url, tracker_group_id, comment=None, css_selector=None,frequency=None):
        
# Make sure there is a corresponding webpage record. Create if there is none.

        my_url = normalize_url(url)
        if session.query(Webpage).filter(Webpage._url == my_url).count() == 0:
            self.webpage_insert(session, my_url)

# Default selector and frequency.

        if not css_selector:
            css_selector = self.default_tracker_css_selector

        if not frequency:
            frequency = self.default_tracker_frequency

        my_url = normalize_url(my_url)

# Create the tracker.

        t = Tracker(name=name, url=my_url,frequency=frequency, tracker_group_id=tracker_group_id,comment=comment, css_selector=css_selector)
        session.add(t)
  
    def user_insert (self,session,email,first_name,last_name,password,full_name=None, roles=None):      
        u = User(email=email,first_name=first_name,last_name=last_name, password=password,full_name=full_name, roles=roles)
        session.add(u)
    # Return new used ID
        my_query = session.query(User).filter(User.email == email).first()
        my_id = my_query.id
        return my_id
        

    def webpage_insert (self, session, url_arg):
#        my_ok = self.exists_check("webpage","url",url_arg)
        w = Webpage(url=url_arg)
        session.add(w)
    