'''
Pools experimentation

14-06-2012, Andy    NEW
14-06-2012, Andy    Improved comments

Experiments with Pool 

You can adjust pool_params.threads to change number of async processes and see how behaviour changes.

TESTING

In TERMINAL window

To use the 'flush' method whereby sync workers are used to flush the pool:

python -m unittest test_pools.testing.test_flush

To use the 'close/join' method:

python -m unittest test_pools.testing.test_close

DEBUGGING

Can be run in Eclipse. Both tests will run (obviously) but this is not a problem.


'''

import os

from array import *

from email.mime.text import MIMEText
from traceback import format_exc
from multiprocessing.dummy import Pool


from time import sleep
import smtplib

import unittest 

def smtp_params():
    null = 0

smtp_params.notify = 'notify@polardog.co.uk'
smtp_params.sender = 'kgenie@polardog.co.uk'
smtp_params.server ='mail.a222.co.uk'
smtp_params.port = 587
smtp_params.username = 'oval@a222.co.uk'
smtp_params.password = 'gates98'

def pool_params():
    null = 0
pool_params.threads = 2

def pool_tracker():
    null = 0   
pool_tracker.list = []
pool_tracker.shutdown = 0

def pool_shutdown ():
    sleep(1)
    pool_tracker.shutdown = pool_tracker.shutdown + 1
    show_test(pool_tracker.shutdown,"Shutdown") 

def pool_test (test_no,sleep_for):
    pool_tracker.list.append(test_no)
    sleep(sleep_for)
    mail_charset = "utf-8"
    mail_mime = "PLAIN"
    mail_content = "Mail content"
    msg = MIMEText(mail_content, mail_mime, mail_charset)
    
    mail_to = "any@polardog.co.uk"
    
    msg['Subject'] = "Test %s" % str(test_no)
                
    msg['From'] = mail_to
    msg['to'] = mail_to
    
    if True:
        print "Sending mail for %s" % str(test_no)
        conn = smtplib.SMTP(smtp_params.server, smtp_params.port)
        conn.ehlo()
        conn.login(smtp_params.username, smtp_params.password)
        conn.sendmail(smtp_params.sender, [mail_to], msg.as_string())
        conn.quit()
    
    show_test(test_no,"Completed(" + str(sleep_for) + " seconds)")
    pool_tracker.list.remove(test_no)
    
def pool_test_all(with_flush):
    print " "
    if with_flush:
        print "FLUSH"
    else:
        print "CLOSE/JOIN"
        
    pool = Pool(pool_params.threads)

    test_max = pool_params.threads * 3
    my_test = 0

    while my_test < test_max:
        my_test = my_test + 1
        my_sleep = test_max - my_test + 1
        my_worker = pool.apply_async(pool_test, args = (my_test,my_sleep))
        show_test(my_test,"Queued")

    my_test = 0
    test_max = pool_params.threads + 1
    if with_flush:
        print "Pool FLUSH shutdown"
        while my_test < test_max:
            my_test = my_test + 1
            my_worker = pool.apply(pool_shutdown)
        print "Flushed"
    else:
        print "Pool CLOSE/JOIN shutdown"
        pool.close()
        print "Closed"
        pool.join()
        print "Joined"
    
    worker_count = 1
    old_count = 0

    while worker_count > 0:
        worker_count = len(pool_tracker.list)
        if worker_count == old_count:
            print "."
        else:
           old_count = worker_count
           print "Remaining: " + str(worker_count)
        sleep(8)
    
    print "All done"
    
def show_test (test_no, arg_text):
    print str(test_no) + " " + arg_text
    
class testing(unittest.TestCase):
    
    def test_flush(self):
        pool_test_all(True)
        
    def test_close(self):
        pool_test_all(False)
       
    
if __name__ == '__main__':
    unittest.main()
    