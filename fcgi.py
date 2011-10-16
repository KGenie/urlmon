#!/usr/bin/env python
import env, os
from config import make_app
from flup.server.fcgi import WSGIServer


if __name__ == '__main__':
    wsgi_app = make_app()
    try:
        sock_file='/tmp/urlmon.sock'
        if os.path.exists(sock_file):
            os.remove(sock_file)
        WSGIServer(wsgi_app, bindAddress=sock_file).run() 

    except KeyboardInterrupt:
        # TODO This block will not execute.
        # This is a bug in python which makes the interrupt not be delivered
        # while there are waiting condition objects(as probably in httpserve)
        # this must be worked arround somehow, so the child process are cleanly
        # shut down in case of a interrupt signal.
        print 'this will not execute'
        sys.exit(1)
