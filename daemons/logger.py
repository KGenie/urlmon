import sys, os, fork_vars, glob
from select import select
from time import sleep
from pipestream import PipeStream
from daemon import Daemon

class Logger(Daemon):

    def __init__(self):
        Daemon.__init__(self)
        self.pipestreams = None
        self.logpipes = None
        self.go = None


    def cleanup(self):
        Daemon.cleanup(self)
        self.go = False
        if self.pipestreams:
            for ps in self.pipestreams:
                ps.close()
                os.remove(ps.path)


    def read_data(self, streams):
        buff = []
        for stream in streams:
            for line in stream:
                buff.append(line)
        return "\n".join(buff) + '\n'


    def select(self, streams):
        fds = list(s.fd for s in streams)
        ready, w, x = select(fds, [], [])
        return (s for s in streams if s.fd in ready)


    def run(self):
        pattern = fork_vars.LOG_DIR + '/*.log'
        self.logpipes = list(f for f in glob.glob(pattern))
        self.pipestreams = list(PipeStream(f) for f in self.logpipes)
        logs = self.pipestreams
        self.go = True

        while self.go:
            try:
                ready = self.select(logs)
                data = self.read_data(ready)
                sys.stdout.write(data)
                sys.stdout.flush()
            except Exception, e:
                print >> sys.stderr, 'Error ocurred while receiving message: %s' % e 
      
  
DAEMON = Logger()
