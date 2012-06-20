'''
Daemon using Pool processing. 

20-06-2012, Andy    NEW

Calling process creates a control file (e.g. scraper.txt) and passes this to the startup.
Script then loops until control file is deleted at which point it terminates in a tidy manner.
'''

from database.sqlalch import Session
from multiprocessing.dummy import Pool
from time import sleep

class PoolDaemon(object):

    def daemon_control(self,pool_object,thread_count):
# Replaced by custom code in the inheriting class (unless code here already suits!)
        try:
            self.my_count = self.my_count + 1
            if self.my_count > thread_count:
                self.my_count = 1
        except:
            self.my_count = 1
            
        pool_object.apply_async(self.daemon_process, args=(self.my_count,thread_count))      

   
    def daemon_process(self, thread_no, thread_count):
# Replaced when inherited
        print "Process " + str(thread_no) + " of " + str (thread_count)
        sleep(5)
        print "Process %s ended" % thread_no
                
                
    def start_daemon (self,thread_count,sleep_time, control_file):
# Starts the daemon. Arguments are:
# thread_count (maximum concurrent threads)
# sleep_time (interval between cycles)
# control_file (file which, when deleted by another process, will signal termination)
        daemon_active = True
        my_count = 0    
        print "Running"
        pool = Pool(thread_count)
        print "Running %s threads" % str(thread_count)
        while daemon_active:
            self.daemon_control(pool, thread_count)

# Check control file still exists. If it has been deleted then just stop.
            try:
                my_file = open(control_file, 'r')
                my_file.close
                print "Sleeping for %s seconds" % str(sleep_time)
                sleep(sleep_time)
            except:
                daemon_active = False
        
        print "%s not found: closing down" % control_file
        self.shutdown(pool)
        print "Finished"  

    def shutdown(self,pool):
        print "Closing Pool"
        my_count = 1
    # Count the workers
        for worker in pool._pool:
            my_count = my_count + 1
    # Queue same number (plus 1) of dummy workers
        while my_count > 0:
            my_worker = pool.apply(self.__shutdown_dummy)
            my_count = my_count - 1
        print "Pool Closed"                      
          
        return True
    
    def __shutdown_dummy(self):
        sleep(1)
        

DAEMON = PoolDaemon()
   

        
        