#!/usr/bin/env python
import env
from config import make_app
from paste import httpserver


if __name__ == '__main__':
    wsgi_app = make_app()
    httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)
