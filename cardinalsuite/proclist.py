#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import time

import madre



import Ui_ProcList

class ProcList(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ProcList.Ui_ProcList()
        self.ui.setupUi(self)
        self.ses = madre.ses()
        t = self.ui.tableWidget
        t.setSortingEnabled(True)
        self.ui.bRefresh.clicked.connect(self.refresh)
        self.ui.bKill.clicked.connect(self.kill)
        
    def refresh(self):
        out, err = self.ses.ex("ps -o pid,comm,vsz,rss,args")
        print "procs", out
        t = self.ui.tableWidget        
        lines = out.splitlines()
        t.clear()
        t.setColumnCount(5)
        t.setColumnWidth(4, 400)
        h = t.horizontalHeader()
        h.setStretchLastSection(True)
        t.setRowCount(len(lines))
        for ln,l in enumerate(lines):
            cols = l.split(None, 5)
            for coln, col in enumerate(cols):
                
                if col.isdigit():
                    col = int(col)
                elif col[:-1].isdigit() and col[-1] == 'm':
                    col = int(col[:-1]) * 1000000
                
                wi = QtGui.QTableWidgetItem()
                wi.setData(0,col)
                t.setItem(ln, coln, wi)
    def kill(self):
        t = self.ui.tableWidget
        pid_it = t.item(t.currentRow(), 0)
        pid = pid_it.data(0).toInt()[0]
        print "killing pid", pid
        self.ses.ex_root("kill -9 %s" % pid)
        self.refresh()
        
        
