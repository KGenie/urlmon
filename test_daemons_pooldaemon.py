
'''
Unit test for conceptual pool daemon

20-06-2012, Andy

This script starts the Daemon.

'''
import env 

import config

import os

from daemons.pooldaemon import DAEMON as PoolDaemon 

import time

import unittest

#########################################################################################


  
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

def test_file(create_file=False):
    my_file = "pooldaemon.txt"
    if create_file:
        f = open (my_file,"w")
        f.close
    return my_file

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

def test_name_lc (no_inc=False):
# Retrieve test name. Return in lower case with spaces converted to underscore. Intended to make this friendly as part of Email or URL
    if no_inc:
        my_name = test_iteration.name
    else:
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

    

class testing(unittest.TestCase):
    
    
   
    def test_pooldaemon_start(self):
        test_name("Start pooldaemon")
        control_file = test_file(True)
        print "RM %s manually to stop" % control_file
        PoolDaemon.start_daemon(3,2, control_file)
            
if __name__ == '__main__':
    unittest.main()

    