import logging, urllib2
from multiprocessing import Pool
from threading import RLock
from tasks.response_processor import process
from time import sleep
from datetime import datetime

log = logging.getLogger(__name__)

__pool = None
__url_cache = None
__cache_lock = None


def initialize():
    thread_count = 1
    global __pool, __url_cache, __cache_lock
    __pool = Pool(thread_count)
    __url_cache = {}
    __cache_lock = RLock()


def retrieve_url(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0')
    response = urllib2.urlopen(request)
    body = process(response)
    return body 


def start_retrieving_url(url):
    retrieve = True
    now = datetime.now()
    if url in __url_cache:
        last_retrieved = __url_cache[url]['date']
        delta = now - last_retrieved 
        if delta.seconds < 360:
            retrieve = False
    if retrieve:
        async_result = __pool.apply_async(retrieve_url, (url,))
        __cache_lock.acquire()
        __url_cache[url] = { 'date': now, 'callback': async_result.get }
        __cache_lock.release()


def finish_retrieving_url(url):
    get_func = None
    __cache_lock.acquire()
    if url not in __url_cache:
        assert False, 'URL retrieval was not requested by this thread'
        start_retrieving_url(url)
    get_func = __url_cache[url]['callback']
    __cache_lock.release()
    return get_func()
