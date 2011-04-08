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
        self.ui.bStartStop.clicked.connect(self.toggle_trace)
        self.postproc = []

        self.ui.bSignal.addActions([
            self.ui.actionSigKill,
            self.ui.actionSigAbort,
            self.ui.actionSigSegv
            ])
    
        def sigkill():
            self.send_signal(9)
        def sigabort():
            self.send_signal(6)
        def sigsegv():
            self.send_signal(11)
            
        self.ui.actionSigAbort.triggered.connect(sigabort)
        self.ui.actionSigKill.triggered.connect(sigkill)
        self.ui.actionSigSegv.triggered.connect(sigsegv)
        
        self.trace_enabled = False
        
        
    
    def send_signal(self, signal):
        self.ses.ex_root('kill -%s %s' % (signal, self.pid()))        
    
    def toggle_trace(self):
        pass
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
        
    def pid(self):
        return self.state['pid']
    def setState(self, rstate):
        self.state = rstate
        self.setWindowTitle(self.state['cmd'] + " " + self.state['pid'])
                
    def setRunner(self, r):
        self.runner = r
        
    def add_postproc(self, title, f):
        self.postproc.append((title,f))
        act = QtGui.QAction(title, self.ui.bPostProc)
        def callback():
            f(self.state)            
            
        act.triggered.connect(callback)
        self.ui.bPostProc.addAction(act)
        
    def set_toggle_act(self,enable_s, disable_s,f):
        """ will call f(state, "enable") """
        
        if f is None:
            self.ui.bStartStop.setEnabled(False)
            
        self.toggle_act = f
        self.enable_s = enable_s
        self.disable_s = disable_s

    def toggle_trace(self):
        if self.trace_enabled:
            self.ui.bStartStop.setText(self.enable_s)
            self.toggle_act(self.state, "disable")
            self.trace_enabled = False
        else:
            self.trace_enabled = True
            
            self.ui.bStartStop.setText(self.disable_s)
            self.toggle_act(self.state, "enable")
        
        
        
