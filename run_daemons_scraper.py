
'''
Script to start and stop 'scraper' daemon

20-06-2012, Andy

This script starts the Daemon.

'''
import env 

import config

import os

from daemons.scraper import DAEMON as ScraperDaemon 

from time import sleep


print "Start scraperdaemon"
control_file = "scraper.txt"
pid = os.fork()
if pid <= 0:
    ScraperDaemon.start_daemon(3,2, control_file)
else:
    sleep(11)
    print           
    print "** Stop scraperdaemon"
    print "** Deleting %s" % control_file
    try:
        os.remove(control_file)
    except:
        pass
    
    