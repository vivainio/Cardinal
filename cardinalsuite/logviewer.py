#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import Ui_LogViewer
import os, re

import logging
import threadutil

class CallbackLogHandler(logging.Handler):    
    """
    A handler class which sends log strings to a wx object
    """
    def __init__(self):
        """
        Initialize the handler
        @param qtDest: the destination object to post the event to 
        
        """
        logging.Handler.__init__(self)
        self.level = logging.DEBUG

    def flush(self):
        """
        does nothing for this handler
        """

    def set_callback(self, cb):
        self.cb = cb

    def emit(self, record):
        """
        Emit a record.

        """
        try:
            msg = self.format(record)
            self.cb(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
            

class LogViewer(QtGui.QWidget):

    def log_line(self, msg):
        """ run in main thread """
        
        self.ui.teLog.appendPlainText(msg)
        
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_LogViewer.Ui_LogViewer()
        self.ui.setupUi(self)
        
        def do_cb(msg):
            #print "Logged one",msg
            def L():
                self.log_line(msg)
            QtCore.QTimer.singleShot(0,L)
                
            
            
        self.hnd = CallbackLogHandler()
        self.hnd.set_callback(do_cb) 
        l = logging.getLogger()
        l.addHandler(self.hnd)

    