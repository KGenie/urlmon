#!/usr/bin/env python
import env
from config import make_app
from paste import httpserver


if __name__ == '__main__':
    wsgi_app = make_app()
    try:
        httpserver.serve(wsgi_app, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        # TODO This block will not execute.
        # This is a bug in python which makes the interrupt not be delivered
        # while there are waiting condition objects(as probably in httpserve)
        # this must be worked arround somehow, so the child process are cleanly
        # shut down in case of a interrupt signal.
        print 'this will not execute'
        sys.exit(1)
         
