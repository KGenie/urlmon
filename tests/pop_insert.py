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
    
        
    def exists_check (self, arg_table, arg_column, arg_key):
        my_table = Table(arg_table, metadata, autoload=True)
        my_query = arg_column + "= '" + arg_key + "'"
        sql = my_table.select(my_query)
        rs = sql.execute()
        row = rs.fetchone()
        if row:
            return true
        else:
            return false
    
    def tracker_default (self,css_selector,frequency):
        self.default_tracker_css_selector = css_selector
        self.default_tracker_frequency = frequency
    
    
    def tracker_group_insert (self,session,name,user,comment=None):
    # Insert group, return group id.
        g = TrackerGroup(name=name, user_id=user, comment=comment)
        session.add(g)
        return g
        
    def tracker_insert(self, session, name, url, tracker_group_id, comment=None, css_selector=None,frequency=None):
        
# Make sure there is a corresponding webpage record.
        my_url = url
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
  

    def webpage_insert (self, session, url_arg):
#        my_ok = self.exists_check("webpage","url",url_arg)
        w = Webpage(url=url_arg)
        session.add(w)
    