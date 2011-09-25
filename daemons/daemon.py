# Code based on :
# http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
import os, sys, logging, atexit, fork_vars, time, signal


__logger = logging.getLogger('daemons')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info

class Daemon(object):
   
    def __init__(self, stdin=None, stdout=None, stderr=None):
        self.name = self.__class__.__name__.lower()
        self.pidfile = os.path.join(fork_vars.PID_DIR, self.name + '.pid')
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

   
    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                # Don't exit from the first the parent since it is the
                # web app. Just return since it still has work to do.
                return False
           
        except OSError, e:
            error("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        debug('Checking if should redirect standard file descriptors')
        if self.stdin:
            debug('Redirecting stdin')
            si = file(self.stdin, 'r')
            os.dup2(si.fileno(), sys.stdin.fileno())

        if self.stdout:
            debug('Redirecting stdout')
            sys.stdout.flush()
            so = file(self.stdout, 'a+')
            os.dup2(so.fileno(), sys.stdout.fileno())
        
        if self.stderr:
            debug('Redirecting stderr')
            sys.stderr.flush()
            se = file(self.stderr, 'a+', 0)
            os.dup2(se.fileno(), sys.stderr.fileno())

        # register cleanup code
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, lambda signum, sf: sys.exit(1))

        # write pidfile
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
        return True
   

    def cleanup(self):
        self.delpid()


    def start(self):
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            error("pidfile %s already exist. Daemon already running?" %\
                    self.pidfile)
            return
       
        # Start the daemon
        is_daemon = self.daemonize()
        if is_daemon:
            self.run()


    def delpid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)


    def stop(self):
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            error("pidfile %s does not exist. Daemon not running?" %\
                    self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process       
        try:
            os.kill(pid, signal.SIGTERM)
            #while 1:
            #    time.sleep(0.1)
        except OSError, e:
            err = str(e)
            if err.find("No such process") > 0:
                self.delpid()
            else:
                error(err)
                return
        finally:
            self.delpid()
                            

    def restart(self):
        self.stop()
        self.start()


    def run(self):
        # override
        pass
