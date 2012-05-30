'''
Mail Service

29-05-2012, Andy    NEW

Sends mail asychronously (but pool process still being understood)

'''

import smtplib, logging, app_globals, os
from traceback import format_exc
from multiprocessing.dummy import Pool
from email.mime.text import MIMEText

from app_components.service import Service

__logger = logging.getLogger('daemons.controllable.mailer')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info

def smtp_params():
    null = 0

smtp_params.sender = 'kgenie@polardog.co.uk'
smtp_params.server ='mail.a222.co.uk'
smtp_params.port = 587
smtp_params.username = 'oval@a222.co.uk'
smtp_params.password = 'gates98'

class MailerService(Service):
    
    def __send_mail (self, mail_to, mail_subject, mail_content="", mail_mime='PLAIN', mail_charset='utf-8',mail_from=None):
    # Send a mail in specified format. Argument mail_from may be used to override the default 'from' mail in the SMTP setup.
        
    # Defaulting does not seem effective, coded here to compensate:
        if not mail_charset:
            mail_charset = "utf-8"
        
        if not mail_mime:
            mail_mime = "PLAIN"
                
        
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
        return True
        
        
    def send_mail (self, mail_to, mail_subject, mail_content=None, mail_mime=None, mail_charset=None,mail_from=None):
        self.threads = 3
        self.pool = Pool(self.threads)
        
        my_print = self.pool.apply_async(self.__send_mail, args=(mail_to, mail_subject, mail_content, mail_mime, mail_charset,mail_from))
        
        return 1
