#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import time,os

import madre

import threadutil
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
        self.state = None
        self.trace = None
                    

    def external_editor(self):
        os.system("gedit %s &" % self.tgtfile)
        
    def set_trace_info(self, state, trace_to_track):
        self.state = state
        self.trace = trace_to_track
        self.srcfile = self.state['state'] + "/" + self.trace
        self.tgtfile = self.state['hostdir'] + "/" + self.trace
        self.refresh()
                
    def start_tracking(self, remote_file):
        cmd = 'tail -f ' + remote_file
        self.ch = self.ses.invoke_shell()
        self.ch.send(cmd + "\n")
        pte = self.ui.plainTextEdit
        def frag(s):            
            pte.moveCursor(QtGui.QTextCursor.End)
            pte.insertPlainText(s)
            
        def reader():
            return self.ch.recv(200)
            
        self.repeater = threadutil.Repeater(reader)
        self.repeater.fragment.connect(frag)
        self.repeater.start()
        
    def start_tracking_fobj(self,fobj):
        pte = self.ui.plainTextEdit
        
        def dump_lines(lines):
            print "l",len(lines)
            pte.moveCursor(QtGui.QTextCursor.End)
            pte.insertPlainText("\n".join(lines))
        
        nl = threadutil.NowOrLater(dump_lines)    
        
        def frag(line):
            nl.add(line.rstrip('\n'))            
            
        def reader():
            line = fobj.readline()
            if not line:
                
                raise StopIteration
            return line        
                

        self.repeater = threadutil.Repeater(reader)
        self.repeater.fragment.connect(frag)
        self.repeater.start()
        
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
    