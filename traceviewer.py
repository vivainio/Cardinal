#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import time

import madre

from threadutil import RRunner

import Ui_TraceViewer

class TraceViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_TraceViewer.Ui_TraceViewer()
        self.ui.setupUi(self)
        self.ses = madre.ses()

    def set_trace_info(self, state, trace_to_track):
        self.state = state
        self.trace = trace_to_track
        self.srcfile = self.state['state'] + "/" + self.trace
        self.tgtfile = self.state['hostdir'] + "/" + self.trace
        self.refresh()
        
        
    def refresh(self):
        def run():
            time.sleep(2)
            self.ses.get(self.srcfile, self.tgtfile)
            
        def ready():
            cont = open(self.tgtfile).read()
            print "got cont"
            print cont
            self.ui.plainTextEdit.setPlainText(cont)
                    
        #r = self.r = RRunner(run)
        #r.finished.connect(ready)
        #self.r.start()
        run()
        ready()
        
        
        
        
        
