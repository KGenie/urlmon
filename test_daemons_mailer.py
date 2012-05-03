
'''
Created on Mar 31, 2012

@author: bernard
'''

'''
Unit Test for Notifications

This is an initial shallow test. It tests basic functions,e.g : Is record created? Does it retrieve?
It does not do comprehensive tests on every single column.

Be warned: produces many rows of data! 

NOTE. You can change the destination email and return address by altering mail_args 

'''
import env 

import config

import os

from daemons.mailer import DAEMON as mailer_daemon

import time

import unittest

#########################################################################################



def generate_email():
    return test_name_lc() + "@kgenie.com"


    
def print_number (my_text, my_number):
# Prints text then a number. Handles number if null or non-numeric.
        if my_number:
            try:
                my_show = str(my_number)
            except:
                my_show = "None!"
        else:
            my_show = "None!"
        print my_text + ": " + my_show

def test_iteration():
# Holder for test name and number.
    null = 0
    
test_iteration.counter = 0
test_iteration.name = ""

def test_name(my_name=None):
# If Name supplied, change current test to supplied name.
    if my_name:
        test_iteration.name = my_name
        print " "
        print "Test: " + my_name
# Return test name appending unique number
    return test_iteration.name + "_" + str(test_next())

def test_name_lc ():
# Retrieve test name. Return in lower case with spaces converted to underscore. Intended to make this friendly as part of Email or URL
    my_name = test_name()
    my_name = my_name.lower()
    my_name = my_name.replace(" ", "_")
    return my_name

def test_next():
# Increment stored counter each time this is called.  
    test_iteration.counter = test_iteration.counter + 1
    return test_iteration.counter

def test_prefix(my_prefix):
# increment counter and return appended to supplied string.
    return my_prefix + "_" + str(test_next())


def run_before():
    print "Pre test"
    stop_mailer()
    start_mailer()
    


#########################################################################################

def start_mailer():
    parent_pid = os.getpid()
    config.start_daemon(mailer_daemon, parent_pid)
    print "Daemon starting, please wait"
# Add a delay to enable mailer to get going.
    time.sleep(5)
    print "Daemon started (in theory)"
    

def stop_mailer():
    mailer_daemon.stop()
    print "Daemon stopping"
    time.sleep(5)
    print "Daemon stopped (in theory)"
    

class testing(unittest.TestCase):

    def test_charset(self):
        test_name("Charset test")
        mail_to = test_prefix("kg") + "@a222.biz"
        mail_subject = test_name()
        mail_charset = "shift-jis"
        mail_mime = "PLAIN"
        mail_content = mail_subject + " Japanese: " + mail_charset
        my_result = mailer_daemon.send_mail (mail_to, mail_subject, mail_content, mail_mime, mail_charset)
        print "Mail details"
        print mail_to
        print mail_subject
        print mail_content
        print mail_mime
        print mail_charset
        self.assertEqual(my_result,1)
   
    
    def test_default(self):
        test_name("Default settings")
        mail_to = test_prefix("kg") + "@a222.biz"
        mail_subject = test_name()
        mail_charset = "utf-8"
        mail_mime = "PLAIN"
        mail_content = mail_subject + " " + mail_mime + " " + mail_charset
        my_result = mailer_daemon.send_mail (mail_to, mail_subject, mail_content)
        print "Mail details"
        print mail_to
        print mail_subject
        print mail_content
        print mail_mime
        print mail_charset
        self.assertEqual(my_result,1)        
    
    def test_from(self):
        test_name("Specific FROM address")
        mail_to = test_prefix("kg") + "@a222.biz"
        mail_from = test_prefix("kgfrom") + "@a222.biz"
        mail_subject = test_name()
        mail_content = mail_subject + " "  + mail_from
        my_result = mailer_daemon.send_mail (mail_to, mail_subject, mail_content, None, None, mail_from)
        print "Mail details"
        print mail_to
        print mail_subject
        print mail_content
        print mail_from
        self.assertEqual(my_result,1)
    

            
    def test_mime(self):
        test_name("MIME test")
        mail_to = test_prefix("kg") + "@a222.biz"
        mail_subject = test_name()
        mail_charset = "utf-8"
        mail_mime = "HTML"
        mail_content = mail_subject + " " + mail_mime + " " + mail_charset
        my_result = mailer_daemon.send_mail (mail_to, mail_subject, mail_content, mail_mime)
        print "Mail details"
        print mail_to
        print mail_subject
        print mail_content
        print mail_mime
        print mail_charset
        self.assertEqual(my_result,1)
        


run_before()

if __name__ == '__main__':
    unittest.main()


    