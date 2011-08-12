import env
from multiprocessing import Process
from time import sleep
import fork_vars

def remote_call():
    from services.tracker import TrackerService
    serv = TrackerService(None)
    print list(serv.get_all())
    print 'this was a remote call'


def spawn():
    p = Process(target=remote_call)
    p.start()
    from services.tracker import TrackerService
    p.join()
