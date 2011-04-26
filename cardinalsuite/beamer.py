#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import QMessageBox
import madre

import Ui_Beamer
import os, re

from cardinalutil import *
from threadutil import log_filedes
import logging
import urllib


log = logging.getLogger("crd.beamer")

class Beamer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Beamer.Ui_Beamer()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.ses = madre.ses()
        self.set_icon()
        
        self.inbox = self.ses.rootdir() + "/inbox"
        self.outbox = self.ses.rootdir() + "/outbox"
        self.ses.ex('mkdir -p ' + self.inbox)
        self.ui.bFetchOutbox.clicked.connect(self.fetch_outbox)
        self.ui.bDropClipboard.clicked.connect(self.drop_clipboard)
        self.cb = QtGui.QApplication.clipboard()
        
    def set_icon(self):
        self.setWindowIcon(QtGui.QIcon(iconpath() + "/go-down.png"))    
        
    def drop_clipboard(self):
        md = self.cb.mimeData()
        
        self.drop_mime(md)
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
        self.gen_action(str(f))
        self.send_file(str(f))
        

    def send_file(self,f):
        self.ses.put(f, self.ses.rootdir() + '/inbox/' + os.path.basename(f))
        
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
                
                out, err = self.ses.pkg_install(installs)
                log_filedes(out, logging.DEBUG)
                log_filedes(err, logging.WARNING)
        
        pass
    
    
    def fetch_url(self, url):
        
        tgtdir = cachedir() + "/fetched"
        basename = os.path.basename(str(url.path()))
        if not os.path.isdir(tgtdir): os.makedirs(tgtdir)
        newf = '%s/%s' % (tgtdir, basename)
        surl = str(url.toString())
        log.info("Fetch " + surl +" => " + newf)
        urllib.urlretrieve(surl,  newf )
        return newf
                           

    def gen_action(self, locf):
        if locf.endswith('.deb') or locf.endswith('.rpm'):
            self.actions.append(('install', self.inbox + "/" + os.path.basename(locf) ))
        
    def drop_mime(self, mimedata):
        urls = mimedata.urls()
        if not urls: return

        self.actions = []
        for z in urls:
            url = QtCore.QUrl(z)
            scheme = url.scheme()
            if scheme == 'http':
                
                locf = self.fetch_url(url)
                self.drop_file(locf)
            
            elif scheme == 'file':
                locf = str(url.toLocalFile())
                self.drop_file(locf)                
                
            else:
                log.warn("Drop ignored: " + `z`)
        
        self.hnd_actions(self.actions)
            
    def dropEvent(self, ev):
        #print "Dropping",ev
        md = ev.mimeData()
        self.drop_mime(md)
