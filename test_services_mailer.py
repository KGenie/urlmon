
'''

28-May-2012, Andy, new file. 
04-Jun-2012, Andy, removed incorrect comments.

'''

'''
Unit test for mailer service.

NOTE. You can change the destination email and return address by altering mail_args 

'''
import env 

import config

import os

from services.mailer import MailerService

import time



#########################################################################################



def generate_email():
    return test_name_lc() + "@kgenie.com"

def get_mailto(arg_string):
    return arg_string + "_kg@triumphacclaim.co.uk"
    
    
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

def test_results (mail_to,mail_subject, mail_content,  mail_charset,  mail_mime, mail_from):
    print "To:" + mail_to
    print "Subject:" + mail_subject
    print "Content:" + mail_content
    print "Charset:" + mail_charset
    print "Mime:" + mail_mime
    print "From:" + mail_from

    #########################################################################################

    

class testing():
    
    def test_charset_japanese(self):
        test_name("Charset Japanese test")
        mail_to = get_mailto(test_prefix("kg"))
        mail_subject = test_name()
        mail_charset = "shift-jis"
        mail_mime = "PLAIN"
        mail_from = "(default)"
        mail_content = mail_subject + " Japanese: " + mail_charset
        my_service = MailerService
        my_result = MailerService(my_service).send_mail (mail_to, mail_subject, mail_content, None, mail_charset)
        test_results (mail_to,mail_subject, mail_content,  mail_charset,  mail_mime, mail_from)
        my_result.get()
   
    def test_from(self):
        test_name("Specific FROM address")
        mail_to = get_mailto(test_prefix("kg"))
        mail_from = test_prefix("kgfrom") + "@polardog.co.uk"
        mail_subject = test_name()
        mail_mime = "PLAIN"
        mail_charset = "utf-8"
        mail_content = mail_subject + " "  + mail_from
        my_service = MailerService
        my_result = MailerService(my_service).send_mail(mail_to, mail_subject, mail_content, None, None, mail_from)
        test_results (mail_to,mail_subject, mail_content,  mail_charset,  mail_mime, mail_from)
        my_result.get()

            
    def test_mime_html(self):
        test_name("MIME test")
        mail_to = get_mailto(test_prefix("kg"))
        mail_subject = test_name()
        mail_charset = "utf-8"
        mail_mime = "HTML"
        mail_from = "(default)"
        mail_content = mail_subject + " " + mail_mime + " " + mail_charset
        my_service = MailerService
        my_result = MailerService(my_service).send_mail(mail_to, mail_subject, mail_content, mail_mime)
        test_results (mail_to,mail_subject, mail_content,  mail_charset,  mail_mime, mail_from)
        my_result.get()
    
    for each_method in dir():
        if each_method[:5] == "test_":
            my_command = each_method + "(-1)"
            exec my_command
    
       
       
print "Please check email for results"
    