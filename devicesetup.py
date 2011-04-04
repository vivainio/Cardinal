#!/usr/bin/env python

from PyQt4 import QtGui
import sys,os

import madre

ses = madre.ses()

class SetupWiz(QtGui.QWizard):
    def __init__(self, parent = None):
        QtGui.QWizard.__init__(self, parent)
        

def startpage():
    p = QtGui.QWizardPage()
    l = QtGui.QGridLayout()
    p.setLayout(l)
    ipf = QtGui.QLineEdit()
    ipf.setText("192.168.2.15")
    lab = QtGui.QLabel("Host address")
    l.addWidget(ipf, 0, 1)
    l.addWidget(lab, 0,0)
    
    print l
    p.setTitle("MAD Developer startup")
    p.setSubTitle("Please start MAD Developer on device and try to get ip address")
    return p

class ConnectingPage(QtGui.QWizardPage):
    def __init__(self, parent= None):
        QtGui.QWizardPage.__init__(self, parent)
        self.ok = False
    def isComplete(self):
        print "iscmpl"
        return False
    def initializePage(self):
        print "Page init"
        
        r = os.system("ping 192.168.2.15")
        print "ret", r
        if r:
            self.ok = False
            
            self.setSubTitle("Connection failed. Go back to previous stage")
            return
        
        
        ses.copykey()
    
def connecting_page():
    p = ConnectingPage()
    p.setTitle("Connecting")
    return p
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)    
    
    w = SetupWiz()
    w.addPage(startpage())
    w.addPage(connecting_page())
    
    w.show()
    sys.exit(app.exec_())



