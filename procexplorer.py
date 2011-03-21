import sys,os
from PyQt4 import QtCore, QtGui

import madre

import Ui_ProcExplorer

import traceviewer

class ProcExplorer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProcExplorer.Ui_ProcExplorer()
        self.ui.setupUi(self)
            
            
    def setState(self, rstate):
        self.parseState(rstate[0])
        self.setWindowTitle(self.state['cmd'] + " " + self.state['pid'])
        self.logs = ['out', 'err']
        cloc = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.CacheLocation))
        self.hoststate = cloc + "/" + self.state['pid']
        if not os.path.isdir(self.hoststate):
            os.makedirs(self.hoststate)
            self.state['hostdir'] = self.hoststate
        
        for l in self.logs:
            log = traceviewer.TraceViewer()
            t = self.ui.tabWidget.addTab(log, l)
            log.set_trace_info(self.state, l)
        
    def parseState(self, s):
        lines = s.splitlines()
        d = {}
        for l in lines:
            pts = l.split("=",1)
            if len(pts) == 2:
                d[pts[0].strip()] = pts[1].strip()
                
        self.state = d
        
    def setRunner(self, r):
        self.runner = r
    
