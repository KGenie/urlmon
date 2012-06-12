'''
Mail Service

29-05-2012, Andy    NEW

Sends mail asychronously via Pool module.
Returns the Pool Worker object. 
This can be processed by the caller to ensure that mailing has been completed.

'''

import smtplib, logging, app_globals, os
from traceback import format_exc
from multiprocessing.dummy import Pool

from email.mime.text import MIMEText

from storage import StorageService

def pool_params():
    null = 0

pool_params.threads = 2    

def shutdown_params():
    null = 0

shutdown_params.email = "end@triumphacclaim.co.uk"
shutdown_params.subject = "Mailer shutdown"

def smtp_params():
    null = 0

smtp_params.notify = 'notify@polardog.co.uk'
smtp_params.sender = 'kgenie@polardog.co.uk'
smtp_params.server ='mail.a222.co.uk'
smtp_params.port = 587
smtp_params.username = 'oval@a222.co.uk'
smtp_params.password = 'gates98'

class MailerService(StorageService):
    
    def __init__(self,*args, **kwargs):
        self.pool = Pool(pool_params.threads)

    def __no_operation(self):
# Dummy call used in shutdown
        pass
    
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
# Creates an async worker to process the call. Returns worker object.
        my_print = self.pool.apply_async(self.__send_mail, args=(mail_to, mail_subject, mail_content, mail_mime, mail_charset,mail_from))
        return my_print
    
    
    def shutdown (self):
# Flush the pool by running dummy processes
# Using pool size plus one ensures flushing.
        my_count = pool_params.threads + 1
        while my_count > 0:
            my_subject = shutdown_params.subject + "-" + str(my_count)
            my_worker = self.pool.apply_async(self.__send_mail, args=(shutdown_params.email, my_subject))
            my_worker.get()
            my_count = my_count - 1
# Closes down the pools.
        self.pool.close()
        self.pool.join()
              
        