import os, logging, fork_vars
from traceback import format_exc
from multiprocessing.connection import Listener, Client
from multiprocessing.dummy import Pool as ThreadPool
from daemon import Daemon


__logger = logging.getLogger('daemons.controllable')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info

class ControllableDaemon(Daemon):

    CLOSE_CONNECTION = 'CLOSE_CONNECTION'

    def __init__(self, stdin='/dev/null', stdout='/dev/null', 
            stderr='/dev/null'):
        Daemon.__init__(self, stdin, stdout, stderr)
        sockfilename = '%s.socket' % self.name
        self.sockfilename = os.path.join(fork_vars.IPC_SOCKET_DIR, 
                sockfilename)
        self.listener = None
        self.current_connection = None
        self.pool = None
        self.go = None
        self.use_pool = True
        

    def cleanup(self):
        self.go = False
        Daemon.cleanup(self)
        if self.listener:
            self.listener.close()


    def send(self, message, get_response=False):
        response = None
        conn = Client(self.sockfilename, 'AF_UNIX')
        if not get_response:
            if hasattr(message, '__iter__'):
                message = list(message)
            else:
                message = [message]
            message.append(self.CLOSE_CONNECTION)
        conn.send(message)
        if get_response:
            response = conn.recv()

        return response

 
    def process_message(self, message):
        return 'NOT IMPLEMENTED'

        
    def serve_connection(self, connection):
        try:
            message = connection.recv()
            debug('Message received, checking if a response is expected')
            respond = True
            if isinstance(message, list):
                if message[-1:][0] == self.CLOSE_CONNECTION:
                    debug('Close connection requested, not responding')
                    message = message[:-1]
                    respond = False
            response = self.process_message(message)
            debug('Message successfully processed')
            if respond:
                debug('Sending response')
                connection.send(response)
                debug('Response successfully sent')
        except Exception, e:
            error('Error ocurred while receiving message: %s' % format_exc(e)) 
        finally:
            connection.close()


    def init_daemon(self):
        pass


    def run(self):
        try:
            self.init_daemon()
        except Exception, e:
            error('Error ocurred while initializing the daemon %s: %s' %
                    (self.name, format_exc(e)))
        if self.use_pool:
            self.pool = ThreadPool()
        self.listener = Listener(self.sockfilename, 'AF_UNIX')
        self.go = True
        listener = self.listener

        while self.go:
            debug('Waiting for connections...')
            try:
                conn = listener.accept()
                debug('Connection accepted, dispatching to handler')
                if self.use_pool:
                    self.pool.apply_async(self.serve_connection, (conn,))
                else:
                    self.serve_connection(conn)
            except Exception, e:
                error('There was an error in accepting the connection: %s' %
                        format_exc(e))
        if self.use_pool:
            self.pool.close()
            self.pool.join()
