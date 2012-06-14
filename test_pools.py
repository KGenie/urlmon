'''
Mail Service

29-05-2012, Andy    NEW
13-05-2012, Andy    Added reply to .shutdown, added sleep to .shutdown

Sends mail asychronously via Pool module.
Returns the Pool Worker object. 
This can be processed by the caller to ensure that mailing has been completed.

'''

import os

from array import *
from traceback import format_exc
from multiprocessing.dummy import Pool


from time import sleep



def pool_params():
    null = 0
pool_params.threads = 2

def pool_tracker():
    null = 0   
pool_tracker.list = []

def pool_test (test_no,sleep_for):
    pool_tracker.list.append(test_no)
    sleep(sleep_for)
    show_test(test_no,"Completed(" + str(sleep_for) + " seconds)")
    pool_tracker.list.remove(test_no)
    
def show_test (test_no, arg_text):
    print str(test_no) + " " + arg_text
    

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
while my_test < test_max:
    my_test = my_test + 1
    my_worker = pool.apply_async(pool_test, args = (my_test,1))
    show_test(my_test,"Shutdown")

# Wait for last one to complete.
sleep(1)


worker_count = 1
old_count = 0

while worker_count > 0:
    worker_count = len(pool_tracker.list)
    if worker_count == old_count:
        print "."
    else:
        old_count = worker_count
        print "Remaining: " + str(worker_count)
    sleep(1)  
    
    
