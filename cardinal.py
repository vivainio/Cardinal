import sys,os
from PyQt4 import QtCore, QtGui
from threadutil import later

import logging

def setup_logging():

    # Log everything, and send it to stderr.
    logging.basicConfig(level=logging.DEBUG)
    pm = logging.getLogger("paramiko.transport")
    pm.setLevel(logging.INFO)

from proclauncher import ProcLauncher

if __name__ == "__main__":
    setup_logging()
    app = QtGui.QApplication(sys.argv)
    myapp = ProcLauncher()
    myapp.show()
    later(myapp.try_connect)
    #myapp.try_connect()
    logging.debug("App started")
    sys.exit(app.exec_())
