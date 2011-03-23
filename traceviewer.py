#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import time,os

import madre

from threadutil import RRunner, enq_task


import Ui_TraceViewer

class TraceViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_TraceViewer.Ui_TraceViewer()
        self.ui.setupUi(self)
        self.ses = madre.ses()
            
        self.ui.btnRefresh.clicked.connect(self.refresh)
        self.ui.bExternal.clicked.connect(self.external_editor)
                    

    def external_editor(self):
        os.system("gedit %s &" % self.tgtfile)
        
    def set_trace_info(self, state, trace_to_track):
        self.state = state
        self.trace = trace_to_track
        self.srcfile = self.state['state'] + "/" + self.trace
        self.tgtfile = self.state['hostdir'] + "/" + self.trace
        self.refresh()
        
        
    def refresh(self):
        def run():        
            self.ses.get(self.srcfile, self.tgtfile)
            
        def ready():
            cont = open(self.tgtfile).read()
            print "got cont bytes",len(cont)
            #print cont
            self.ui.plainTextEdit.setPlainText(cont)
                    
        r = self.r = RRunner(run)
        r.finished.connect(ready)
        enq_task(r)
    