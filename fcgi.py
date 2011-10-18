#!/usr/bin/env python
import env, os, sys, atexit, fork_vars
from signal import SIGINT
from flup.server.fcgi import WSGIServer
from time import sleep


pid_file = 'fcgi.pid'
socket_file = 'fcgi.socket'
output_file = 'fcgi.log'


def delpid():
    print 'Exiting URL Monitor...'
    if os.path.exists(pid_file):
        os.remove(pid_file)
    if os.path.exists(socket_file):
        os.remove(socket_file)

def daemonize():
    print 'Starting URL Monitor server...'
    pid = os.fork()
    if pid > 0:
        print 'URL Monitor server started successfully on %s' % fork_vars.APP_DIRECTORY
        sys.exit(0)

    os.setsid()
    os.umask(0)


    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    stdin = open('/dev/null', 'r')
    stdout = open(output_file, 'a+')
    stderr = open(output_file, 'a+')
    os.dup2(stdin.fileno(), sys.stdin.fileno())
    os.dup2(stdout.fileno(), sys.stdout.fileno())
    os.dup2(stderr.fileno(), sys.stderr.fileno())

    pid = str(os.getpid())
    pf = open(pid_file, 'w')
    pf.write("%s\n" % pid)
    pf.close()
    atexit.register(delpid)


def start():
    try: 
        pf = open(pid_file, 'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None

    if pid > 0:
        print >> sys.stderr, 'URL Monitor server already started.'
        sys.exit(0)

    daemonize()
    run()


def stop():
    try: 
        pf = open(pid_file, 'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None

    if not pid:
        print >> sys.stderr, 'PID file for the URL Monitor server not found.'
        return

    os.kill(pid, SIGINT)
    
    print 'URL Monitor server stopped successfully'


def run():    
    from config import make_app
    wsgi_app = make_app()

    try:
        if os.path.exists(socket_file):
            os.remove(socket_file)
        WSGIServer(wsgi_app, bindAddress=socket_file, umask=7).run() 

    except KeyboardInterrupt:
        # TODO This block will not execute.
        # This is a bug in python which makes the interrupt not be delivered
        # while there are waiting condition objects(as probably in httpserve)
        # this must be worked arround somehow, so the child process are cleanly
        # shut down in case of a interrupt signal.
        print 'this will not execute'
        sys.exit(1)


def usage():
    print >> sys.stderr, 'Usage : \'./fcgi.py start|stop|restart [virtual_dir]\''
    sys.exit(1)


if __name__ == '__main__':
    l = len(sys.argv)
    if l < 2:
        usage()

    #if l > 2:
    #    virtual_dir = sys.argv[2]
    #    fork_vars.APP_DIRECTORY = '/' + virtual_dir

    command = sys.argv[1]
    if command == 'start':
        start()
    elif command == 'stop':
        stop()
    elif command == 'restart':
        stop()
        sleep(1)
        start()
    else:
        usage()
