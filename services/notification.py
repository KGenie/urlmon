'''
20-04-2012, Andy NEW.
13-06-2012, Andy, added shutdown.

Notification service replaces individual email calls.

Future development will mean notification to a variety of destinations. For the moment this module just emails out notifications (synchronously)

MAINTENANCE NOTE: Various notifications can be turned on and off by changing mail_enabled.

'''

import re

from storage import StorageService



from email.mime.text import MIMEText


from helpers import HtmlHelper, UrlHelper
from jinja2 import Environment, FileSystemLoader

from models.registration import Registration
from models.tracker_group import TrackerGroup
from models.tracker import Tracker
from models.user import User

from services.mailer import MailerService

import smtplib, logging, app_globals, os

uh = UrlHelper()

def make_jinja_email_environment():
    ret = Environment(loader=FileSystemLoader(
        os.path.join(app_globals.APP_ROOT, 'email_templates')))
    ret.globals['h'] = HtmlHelper()
    ret.globals['u'] = UrlHelper()
    return ret

def mail_enabled():
    null = 0
# Set to 0 to turn off feature
mail_enabled.notify_no_tracker = -1
mail_enabled.request_registration = -1
mail_enabled.notify_tracker_updated = -1

def smtp_params():
    null = 0

smtp_params.sender = 'kgenie@a222.biz'
smtp_params.server ='mail.a222.co.uk'
smtp_params.port = 587
smtp_params.username = 'oval@a222.co.uk'
smtp_params.password = 'gates98'
      

def registration_data():
    null = 0

def tracker_data():
    null = 0


class NotificationService(StorageService):
    
    def confirm_registration(self,user_id, base_url):
        if not mail_enabled.request_registration:
            return -1
        
        u = self.session.query(User).get(user_id)
        subject = 'Your account is now active'
        template_name = 'confirm_registration'
        template_context = {'email': u.email, 'url': base_url }
        return self.send_template_mail(u.email, subject, template_name,
        template_context)
        
        
        
        
        
        
    def get_registration_data(self, registration_id):
    # Populate registration_data with tracker related data.
    # This is mindful of future database changes where structure may change.
    # This can be accomodated by changing this def.
        r = self.session.query(Registration).get(registration_id)
        registration_data.email = r.email
        return registration_data
    
    def get_tracker_data(self, tracker_id):
    # Populate tracker_data with tracker related data.
    # This is mindful of future database changes where structure may change.
    # This can be accomodated by changing this def.
        t = self.session.query(Tracker).get(tracker_id)
        tracker_data.css_selector = t.css_selector
        tracker_data.url = t.url
        tracker_data.name = t.name
        g = self.session.query(TrackerGroup).get(t.tracker_group_id)
        tracker_data.group_name = g.name
        tracker_data.user_id = g.user_id
        u = self.session.query(User).get(g.user_id)
        tracker_data.email = u.email
        return tracker_data
    
    
    def notify_no_tracker (self,tracker_id):
    # Send a warning message where tracker no longer relevant
    # Current just sends to email.
        if not mail_enabled.notify_no_tracker:
            return -1
        td = self.get_tracker_data(tracker_id)
        subject = 'Warning: The page at %s has changed, but its tracker must be updated.' % td.url
        template_name = 'tracker_not_found'
        template_context = { 'url': td.url , 'tracker_name' : td.name, 'group_name': td.group_name}
        return self.send_template_mail(td.email, subject, template_name,
        template_context)
        
        
    def notify_tracker_updated (self,tracker_id, old_content, new_content):
    # Send alert message where tracker changed
    # Current just sends to email.
        if not mail_enabled.notify_tracker_updated:
            return -1
        
        td = self.get_tracker_data(tracker_id)
        
              
        subject = 'The page at %s has changed' % td.url
        template_name = 'tracker_updated'
        template_context = { 'url': td.url, 'tracker_name' : td.name, 'group_name': td.group_name, 'old_content': old_content,
            'new_content': new_content }

        return self.send_template_mail(td.email, subject, template_name,
            template_context)
    
    def request_registration(self, reg_id, base_url):
        if not mail_enabled.request_registration:
            return -1
        r = self.get_registration_data(reg_id)
        activation_link = base_url + uh.action(controller='registration', name='confirm_activation',
        reg_id=reg_id)
        subject = 'Activate your account on the Web Monitor'
        return self.send_template_mail(r.email, subject, 'activate',
                {'activation_link': activation_link})
        
        
    def send_template_mail(self, to, subject, template_name,   
        template_context, mime='html', charset='utf-8',mail_from=None):
# Send a templated mail Argument mail_from may be used to override the default 'from' mail in the SMTP setup.
        # Normalize template context
        for k, v in template_context.items():
            if isinstance(v, str):
                template_context[k] = v.decode('utf-8')


        env = app_globals.JINJA_EMAIL_ENV
        templ = env.get_template(template_name + '.jinja2')

        text = templ.render(template_context)
        my_service = MailerService
        return MailerService(my_service).send_mail(to, subject, text, mime, charset, mail_from)
    
    def shutdown(self):
# Shutdown the various services used by notification.
        my_service = MailerService
        return MailerService(my_service).shutdown()
    



app_globals.JINJA_EMAIL_ENV = make_jinja_email_environment()