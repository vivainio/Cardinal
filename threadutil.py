from PyQt4 import QtCore, QtGui



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
    


