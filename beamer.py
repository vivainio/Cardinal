#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import QMessageBox
import madre

import Ui_Beamer
import os, re

from cardinalutil import *
from threadutil import log_filedes
import logging

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
        
    def hnd_actions(self, actions):
        print "Actions",actions
        installs = [t[1] for t in actions if t[0] == 'install']
        
        logging.debug("Maybe install: "+ `installs`)
        if installs:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("You dropped %d installer packages." % len(installs))
            msgBox.setInformativeText("Do you want to install them?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.Yes);
            ret = msgBox.exec_();
            if ret == QMessageBox.Yes:
                
                out, err = self.ses.deb_install(installs)
                log_filedes(out)
                log_filedes(err)
        
        pass
    def dropEvent(self, ev):
        print "Dropping",ev
        md = ev.mimeData()
        urls = md.urls()
        if not urls: return

        actions = []
        for z in urls:
            url = QtCore.QUrl(z)
            scheme = url.scheme()
            if scheme == 'file':
                locf = str(url.toLocalFile())
                if locf.endswith('.deb'):
                    actions.append(('install', self.inbox + "/" + os.path.basename(locf) ))
                        
                self.drop_file(locf)
                
            else:
                print "Ignore drop", z
            self.hnd_actions(actions)