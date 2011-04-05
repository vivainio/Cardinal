#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import madre

import Ui_Beamer
import os, re

from cardinalutil import *


class Beamer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Beamer.Ui_Beamer()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.ses = madre.ses()
        
        self.inbox = madre.crdroot + "/inbox"
        self.outbox = madre.crdroot + "/outbox"
        self.ses.ex('mkdir -p ' + self.inbox)
        self.ui.bFetchOutbox.clicked.connect(self.fetch_outbox)
        
    def fetch_outbox(self):
        ls = self.ses.ls(self.outbox)
        tgtdir = cachedir() + "/outbox"
        if not os.path.isdir(tgtdir): os.makedirs(tgtdir)
        for f in ls:
            src = self.outbox + "/" + f[0]
            tgt = tgtdir + "/" + f[0]
            self.ses.get(src, tgt)
            
        startfile(tgtdir)
        
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
