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
        self.ses = madre.ses()
        self.tabs = {}
        self.ui.bScan.clicked.connect(self.do_scan)
            
    def do_scan(self):
        self.scanTabs()
    def have_tab(self, tab):
        if tab in self.tabs:
            return self.tabs[tab]
                        
        log = traceviewer.TraceViewer()
        t = self.ui.tabWidget.addTab(log, tab)
        log.set_trace_info(self.state, tab)
        self.tabs[tab] = log
        
        return log
        
    def setTabs(self, tabs = []):
        logs = ["out", "err" ]
        logs.extend(tabs)
        for l in logs:
            self.have_tab(l)
                
    def scanTabs(self):
        all = self.ses.ftp.listdir(self.state['state'])
        print "Scanned",all
        for t in all:
            self.have_tab(t)
        
    def setState(self, rstate):
        self.state = rstate
        self.setWindowTitle(self.state['cmd'] + " " + self.state['pid'])
                
    def setRunner(self, r):
        self.runner = r
