'''
Created on Apr 1, 2012

@author: bernard
'''
import env

from daemons.webpage import DAEMON as fetcher_daemon

from services.fetcher import FetcherService

import unittest


class testing(unittest.TestCase):

    def setUp(self):

        fetcher_daemon.start()
              
    def tearDown(self):
        pass

      
    def test_fetcher_fetch_div(self):
        print "Fetcher Fetch"
        my_url = "http://www.electricvanandcar.co.uk/home.html"
        my_service = FetcherService
        my_result = FetcherService(my_service).fetch(my_url,"usual")
        print my_result.url
        my_content = my_result.content
        print my_content
        print "end"

unittest.main()