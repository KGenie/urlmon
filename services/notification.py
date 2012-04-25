from storage import StorageService

from daemons.mailer import DAEMON as mailer_daemon

from email.mime.text import MIMEText

from models.tracker_group import TrackerGroup
from models.tracker import Tracker
from models.user import User

import smtplib, logging, app_globals, os

def smtp_params():
    null = 0

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
        self.send_template_mail(td.email, subject, template_name,
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
        
    def send_mail (self, mail_to, mail_subject, mail_content=None, mail_mime='PLAIN', mail_charset='utf-8',mail_from=None):
        self.smtp_setup()
        msg = MIMEText(mail_content, mail_mime, mail_charset)
        msg['Subject'] = mail_subject
        if mail_from:
            msg['From'] = mail_from
        else:
            msg['From'] = smtp_params.sender
        msg['to'] = mail_to
        
        conn = smtplib.SMTP(smtp_params.server, smtp_params.port)
        conn.ehlo()
        conn.login(smtp_params.username, smtp_params.password)
        conn.sendmail(smtp_params.sender, [mail_to], msg.as_string())
        conn.quit()
        return -1
        
    def send_template_mail(self, to, subject, template_name, 
        template_context, mime='html', charset='utf-8',mail_from=None):

        # Normalize template context
        for k, v in template_context.items():
            if isinstance(v, str):
                template_context[k] = v.decode('utf-8')


        env = app_globals.JINJA_EMAIL_ENV
        templ = env.get_template(template_name + '.jinja2')

        text = templ.render(template_context)
        return self.send_mail(to, subject, text, mime, charset, mail_from)


    def smtp_setup(self):
        smtp_params.sender = 'kgenie@a222.biz'
        smtp_params.server ='mail.a222.co.uk'
        smtp_params.port = 587
        smtp_params.username = 'oval@a222.co.uk'
        smtp_params.password = 'gates98'

        
        return -1