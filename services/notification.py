from storage import StorageService

from daemons.mailer import DAEMON as mailer_daemon

from models.tracker_group import TrackerGroup
from models.tracker import Tracker
from models.user import User

def tracker_data():
    null = 0

class NotificationService(StorageService):
    
    
    def get_tracker_data(self, tracker_id):
    # Populate tracker_data with tracker related data.
    # This is mindful of future database changes where structure may change.
    # This can be accomodated by changing this def. 
        t = self.session.query(Tracker).get(tracker_id)
        tracker_data.css_selector = t.css_selector
        tracker_data.url = t.url
        g = self.session.query(TrackerGroup).get(t.tracker_group_id)
        tracker_data.user_id = g.user_id
        u = self.session.query(User).get(g.user_id)
        tracker_data.email = u.email
        return tracker_data
        
    def notify_no_tracker (self,tracker_id):
    # Send a warning message where tracker no longer relevant
        td = get_tracker_data(tracker_id) 
        debug('Sending warning to %s' % td.email)

        subject = 'Warning: The page at %s has changed, but its tracker must be updated.' % td.url
        template_name = 'tracker_not_found'
        template_context = { 'url': td.url }
        mailer_daemon.send_template_mail(td.email, subject, template_name,
        template_context)
        debug('Warning successfully sent')

    def notify_tracker_updated (self,tracker_id, old_content, new_content):
        td = get_tracker_data(tracker_id)
             
        debug('Sending notification to %s' % td.email)

        subject = 'The page at %s has changed' % td.url
        template_name = 'tracker_updated'
        template_context = { 'url': td.url, 'old_content': old_content, 
            'new_content': new_content }

        mailer_daemon.send_template_mail(td.email, subject, template_name,
            template_context)
        debug('Notification successfully sent')
        
  