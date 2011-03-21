from PyQt4 import QtCore, QtGui

class RRunner(QtCore.QThread):
    def __init__(self, f, parent = None):

        QtCore.QThread.__init__(self, parent)
        self.f = f

    def run(self):
        self.res = self.f()
    


