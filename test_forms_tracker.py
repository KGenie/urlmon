
'''

11-Jun-2012, Andy, new file. 

'''

'''
Test instructions for tracker form.

'''
import env 

import config

import os

from collections import namedtuple


#########################################################################################


def get_url(arg_prefix=None):
    my_url = "www.kgenie.com"
    if arg_prefix:
        return str(arg_prefix) + "www.kgenie.com"
    else:
        return my_url
    
    
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
url_data = namedtuple('url_args','test_name, as_entered resultant')

class test_tracker_form:
    
    def test_http(self):
        url_args = {'test_name' : test_name("HTTP"),
        'as_entered' : get_url("http://") ,
		'resultant' : get_url("http://") ,}
        self.testhelper_url(url_args)

    def test_https(self):
        url_args = {'test_name' : test_name("HTTPS"),
        'as_entered' : get_url("https://") ,
        'resultant' : get_url("https://") ,}
        self.testhelper_url(url_args)

    def test_no_http(self):
        url_args = {'test_name' : test_name("No HTTP"),
        'as_entered' : get_url() ,
        'resultant' : get_url("http://") ,}
        self.testhelper_url(url_args)


    def testhelper_url(self,url_args):
        my_args = url_data(**url_args)
        print
        print "Test " + my_args.test_name
        print "Entered: " + my_args.as_entered
        print "Result:  " + my_args.resultant
       
    def run(self):
      for each_method in dir(self):
        if each_method[:5] == "test_":
            my_command = "self." + each_method + "()"
            exec my_command

print "Please enter url and check per below"
    
if __name__ == '__main__':
  a= test_tracker_form()
  a.run()       
       

    
