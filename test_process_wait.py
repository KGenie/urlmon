
'''
Script to launch batch demons.

30-06-2012, Andy

Daemon start in methods P,Q,R

Files *_process.txt (where * = p/q/r) used to control pool processes. File is created when process starts. Deletion causes process to stop.

TESTING

Needs 2 terminal windows.

TERMINAL 1

Running with join()

python -m unittest test_process_wait.testing.test_join

or without:

python -m unittest test_process_wait.testing.test_no_join

TERMINAL 2 (to stop processing)

python -m unittest test_process_wait.testing.test_stop (stop all)

or

python -m unittest test_process_wait.testing.test_stop_p (stops 'p', can also do stop_q and stop_r)


DEBUGGING

Put a breakpoint at start of method 'p' (call to 'process_create') then invoke via Eclipse.
It is noted that processes q and r start running whilst p halts. There is, however, no obvious debug window relating to the breakpoint.  

'''
import env 

import config

import os

from daemons.mixer import DAEMON as MixerDaemon
from daemons.scraper import DAEMON as ScraperDaemon 
from multiprocessing import Process

import sys

from time import sleep

import unittest

def file_check (control_file):
    
    try:
        my_file = open(control_file, 'r')
        my_file.close
        return True
    except:
        print "File %s missing" % control_file

def file_create (p_name):
    control_file = file_name(p_name)
    f = open (control_file,"w")
    f.close
    print
    print "Created %s" % control_file
    return control_file

def file_delete(p_name):
    control_file = file_name(p_name)
    try:
        os.remove(control_file)
        print "%s deleted" % control_file
    except:
        print "%s already deleted" % control_file

def file_name (p_name):
    return p_name + "_process.txt"

def p ():
    process_create("p",3)

def q():
    process_create("q",4)
    
def r():
    process_create("r",5)

def process_all():
    print "Main process %s" % str(os.getpid())
    
    x = Process(target=p)
    x.start()
    
    x = Process(target=q)
    x.start()

    x = Process(target=r)
    x.start()
    
    return x

def process_create (p_id, p_sleep):
    my_pid = str(os.getpid())
    p_name = p_id + "/" + my_pid 
    print
    print "Process " +  p_name + " started as PID " + my_pid 
    process_loop (p_id, p_name, p_sleep)

def process_loop(p_process, p_name,sleep_time):
    control_file = file_create(p_process)
    while file_check (control_file):
        my_pid = str(os.getpid())
        print "Process %s still running" % p_name
        sleep (sleep_time)
    print "Process %s terminating" % my_pid 

class testing(unittest.TestCase):
    
    def setup(self):
        self.test_stop()
    
    def test_join(self):
        print "Process then join"
        x = process_all()
        x.join()
        sleep(1)
        print "*** Main process %s finishing ***" % str(os.getpid())

    def test_no_join(self):
        print "Process without join"
        process_all()
        sleep(1)
        print "*** Main process %s  still running ***" % str(os.getpid())

    def test_stop(self):
        print "Delete all files"
        self.test_stop_p()
        self.test_stop_q()
        self.test_stop_r()
        
    def test_stop_p(self):
        file_delete("p")
        
    def test_stop_q(self):
        file_delete("q")
        
    def test_stop_r(self):
        file_delete("r")

if __name__ == '__main__':
    unittest.main()
    
    