#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import madre

import Ui_Beamer
import os, re


class Beamer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Beamer.Ui_Beamer()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.ses = madre.ses()
        
        self.inbox = '/home/user/cardinal/inbox'
        self.ses.ex('mkdir -p ' + self.inbox)
        
    def dragEnterEvent(self, e):
        e.accept()

    def drop_file(self,f):
        print "Drop file",f
        self.send_file(str(f))

    def send_file(self,f):
        self.ses.put(f, '/home/user/cardinal/inbox/' + os.path.basename(f))
        
    def dropEvent(self, ev):
        print "Dropping",ev
        md = ev.mimeData()
        urls = md.urls()
        if not urls: return

        for z in urls:
            url = QtCore.QUrl(z)
            scheme = url.scheme()
            if scheme == 'file':
                self.drop_file(url.toLocalFile())
            else:
                print "Ignore drop", z
