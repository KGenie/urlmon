'''
Scraper Daemon using Pool processing. 

20-06-2012, Andy    NEW

'''

from database.sqlalch import Session
from multiprocessing.dummy import Pool
from time import sleep
from daemons.pooldaemon import PoolDaemon

class ScraperDaemon(PoolDaemon):

    def daemon_control(self,pool_object,thread_count):
# Run scraper 1 and 2 concurrently
        pool_object.apply_async(self.scraper1_process)      
        pool_object.apply_async(self.scraper2_process)
# but wait for completion before queueing any more 
        self.shutdown(pool_object)
        
    def scraper1_process(self):

        print "Scraper1 started"
        sleep(5)
        print "Scraper1 ended"
                

    def scraper2_process(self):

        print "Scraper2 started"
        sleep(5)
        print "Scraper2 ended"

DAEMON = ScraperDaemon()
   

        
        