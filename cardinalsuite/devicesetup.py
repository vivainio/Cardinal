#!/usr/bin/env python

from PyQt4 import QtGui
import sys,os

import logging
log = logging.getLogger("devicesetup")

import madre

import crdconfig


ses = madre.ses()

def setup_logging():

    # Log everything, and send it to stderr.
    logging.basicConfig(level=logging.DEBUG)
    pm = logging.getLogger("paramiko.transport")
    pm.setLevel(logging.INFO)

class SetupWiz(QtGui.QWizard):
    def __init__(self, parent = None):
        QtGui.QWizard.__init__(self, parent)
        self.cfg = crdconfig.parse_config()
        self.host = self.cfg['host']
        self.user = self.cfg['user']
        ses.user = self.user
        ses.host = self.host
        

    def startpage(self):
        p = QtGui.QWizardPage()
        l = QtGui.QGridLayout()
        p.setLayout(l)
        ipf = QtGui.QLineEdit()
        ipf.setText(self.host)
        lab = QtGui.QLabel("Host address")
        l.addWidget(ipf, 0, 1)
        l.addWidget(lab, 0,0)
        p.registerField("host", ipf)
        
        cb = QtGui.QCheckBox()
        cblab = QtGui.QLabel("(Re)generate rsa key")
        l.addWidget(cb, 1, 1)
        l.addWidget(cblab, 1,0)
        p.registerField("genkey", cb)
        key = madre.rsa_private_key()
        if not os.path.isfile(key):
            cb.setChecked(True)
        else:
            cb.setToolTip("Key already exists, no need to generate")
            
        #print l
        p.setTitle("Startup - SDK Connectivity")
        p.setSubTitle("Please start SDK connectivity on device and try to acquire " +
                      "IP address (USB / WLAN / ...)")
        return p

    def connecting_page(self):
        p = ConnectingPage()
        p.setTitle("Connecting")
        return p

class ConnectingPage(QtGui.QWizardPage):
    def __init__(self, parent= None):
        QtGui.QWizardPage.__init__(self, parent)
        self.ok = False
        self.setFinalPage(True)
    def isComplete(self):
        #print "iscmpl"
        return self.ok
    def initializePage(self):
        #print "Page init"

        if self.field('genkey').toBool():
            ses.gen_keys()
            
        addr = str(self.field("host").toString())
        #print "conn",addr
        r = os.system("ping -c 1 " + addr)
        
        print "ret", r
        if r:
            self.ok = False
            
            self.setSubTitle("Connection failed. Go back to previous stage")
            return
            
        ses.host = addr
        
        ses.copykey()
        ses.connect()
        ses.setup_remote()
        self.ok = True
        self.setSubTitle("Connection ok. Device initialized")
        self.completeChanged.emit()
        
    
def main():    

    app = QtGui.QApplication(sys.argv)    

    setup_logging()    
    global wiz
    w = wiz = SetupWiz()
    w.addPage(w.startpage())
    w.addPage(w.connecting_page())
    
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

