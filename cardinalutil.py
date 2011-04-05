#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import os

def cachedir():
    cloc = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.CacheLocation)).rstrip("/")
    return cloc + "/cardinal"

def startfile(f):
    os.system("xdg-open " + f)