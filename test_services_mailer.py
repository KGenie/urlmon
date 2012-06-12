
'''

28-May-2012, Andy, new file. 
04-Jun-2012, Andy, removed incorrect comments.
06-jun-2012, Fred, refactored

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
from collections import namedtuple


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

    #########################################################################################

    
#TRICK: using 'mail_from because 'from' is a forbidden variable name in python
mail_data= namedtuple('mail','to subject charset mime mail_from test_name')

class test_mailer_service:
    
    def test_charset_japanese(self):
        mail = {'to' : get_mailto(test_prefix("kg")) ,
		'subject' : test_name() ,
		'charset' : "shift-jis" ,
		'mime' : "PLAIN" ,
		'mail_from' : None , 
		'test_name' : "Charset Japanese test",}
        self.testhelper_sendmail_data(mail)

    def testhelper_sendmail_data(self,mail):
        mail = mail_data(**mail)
        test_name(mail.test_name);
        my_service = MailerService
        my_result = MailerService(my_service).send_mail (mail.to, mail.test_name, str(mail), mail.charset, mail.mime,mail.mail_from)
        print str(mail)
  
   
    def test_from(self):
        mail={ 'test_name' : "Specific FROM address",
               'to' : get_mailto(test_prefix("kg")),
               'mail_from' : test_prefix("kgfrom") + "@polardog.co.uk",
               'subject' : test_name(),
               'mime' : "PLAIN",
               'charset' : "utf-8",}
        self.testhelper_sendmail_data(mail)

    def test_mime_html(self):
        mail={ 'test_name' : "MIME test",
               'to' : get_mailto(test_prefix("kg")),
               'subject' : test_name(),
               'charset' : "utf-8",
               'mime' : "HTML",
               'mail_from' : None,}
        self.testhelper_sendmail_data(mail)
        
    def test_shutdown(self):
        print
        print "Shutdown"
        my_service = MailerService
        my_result = MailerService(my_service).shutdown()
        print "Ensure no Thread exceptions occur. Will need to run several times"
        print "Check that Shutdown emails (see Mailer service module code) are sent after other emails"
        

    def run(self):
      for each_method in dir(self):
        if each_method[:5] == "test_":
            my_command = "self." + each_method + "()"
            exec my_command
    
if __name__ == '__main__':
  a= test_mailer_service()
  a.run()       
       
print "Please check email for results"
    
