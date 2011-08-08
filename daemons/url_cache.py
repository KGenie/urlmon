import logging, signal, urllib2
from BeautifulSoup import BeautifulSoup
from multiprocessing import  Pipe, Process
from multiprocessing.dummy import Pool as ThreadPool
from Queue import Queue
from threading import Thread, Condition, Lock
from time import sleep

log = logging.getLogger(__name__)

_pool = None
_thread_pool = None
_url_cache = None


def initialize():
    process_count = 1
    global _process_pool, _connection_pool, _url_cache, _thread_pool
    _url_cache = {}
    _thread_pool = ThreadPool(processes=process_count)
    _process_pool = Queue(maxsize=process_count)
    for i in range(process_count):
        parent_conn, child_conn = Pipe(duplex=True)
        worker = Process(target=get_urls, args=[child_conn])
        worker.start()
        _process_pool.put((parent_conn, worker))


def get_urls(connection):
    while 1:
        url = connection.recv()
        data = urllib2.urlopen(url).read()
        connection.send((url,data))


def cache_url_async(url):
    connection, worker = _process_pool.get()
    connection.send(url)
    _thread_pool.apply_async(receive_url, (connection, worker))


def receive_url(connection, worker):
    url, data = connection.recv()
    _url_cache[url] = data
    _process_pool.put((connection, worker))
