import logging, os
from select import select


DEFAULT_BUFSIZE = 1024

class PipeStream(object):

    def __init__(self, path, read=True, write=False, encoding='utf-8'):
        if not os.path.exists(path):
            raise Exception('FIFO ''%s'' does not exist!' % path)

        if write:
            mode = os.O_RDWR
        elif read:
            mode = os.O_RDONLY
        else:
            raise Exception('Must open for writing or reading')

        mode = mode | os.O_NONBLOCK
        self.path = path
        self.canread = read
        self.canwrite = write
        self.buff = ''
        self.encoding = encoding
        self.fd = os.open(path, mode)

       
    def __iter__(self):
        return self

    def is_ready(self, block=True):
        if block:
            ready, w, x = select([self.fd],[],[])
        else:
            ready, w, x = select([self.fd],[],[], 0.0001)
        return bool(ready)


    def next(self, size=DEFAULT_BUFSIZE):
        if "\n" in self.buff:
            idx = self.buff.index("\n")
            read = self.buff[:idx]
            self.buff = self.buff[idx+1:]
            return read

        buff = [self.buff]
        stop = False
        while not stop:
            if not self.is_ready(block=False):
                self.buff = ''.join(buff)
                raise StopIteration
            read = self.read(size)
            count = len(read)
            if "\n" in read:
                stop = True
                count = read.index("\n")
                self.buff = read[count+1:]
            buff.append(read[:count])
        return ''.join(buff)


    def read(self, count=DEFAULT_BUFSIZE):
        if not self.canread:
            raise Exception('Not opened for reading')
        if self.is_ready(block=False):
            return os.read(self.fd, count)
        return ''

        
    def write(self, data):
        if not self.canwrite:
            raise Exception('Not opened for writing')
        os.write(self.fd, data)


    def close(self):
        os.close(self.fd)
