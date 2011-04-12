from PyQt4 import QtCore, QtGui

import logging

log = logging.getLogger("out")


class ThreadQueue:
    def __init__(self):
        self.threads = []
        
    def add(self,r):
        empty = not self.threads
        self.threads.append(r)
        r.finished.connect(self.pop)
        if empty:
            r.start()
        
    def pop(self):
        if self.threads:
            ne = self.threads.pop()
            ne.start()

_tq = ThreadQueue()


def enq_task(r):
    _tq.add(r)  
    
class RRunner(QtCore.QThread):
    def __init__(self, f, parent = None):

        QtCore.QThread.__init__(self, parent)
        self.f = f

    def run(self):
        self.res = self.f()
    
class Repeater(QtCore.QThread):
    """ execute f forever, signal on every run """
    
    fragment = QtCore.pyqtSignal(object) 
    
    def __init__(self, f, parent = None):

        QtCore.QThread.__init__(self, parent)
        self.f = f
        
    def run(self):
        while 1:
            res = self.f()
            self.fragment.emit(res)

loggers = []

def log_filedes(f):
    
    def reader():
        line = f.readline()
        if not line:
            raise StopIteration
        log.debug(line.rstrip())
        
    rr = Repeater(reader)
    loggers.append(rr)
    rr.start()

def main():
    # stupid test
    f = open("/etc/passwd")
    log_filedes(f)

if __name__ == "__main__":    
    main()    

