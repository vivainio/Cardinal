#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import os,sys

def cachedir():
    cloc = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.CacheLocation)).rstrip("/")
    return cloc + "/cardinal"

def startfile(f):
    os.system("xdg-open " + f)
    
def pkgpath():
    return os.path.dirname(sys.modules['cardinalsuite'].__file__)
    
def iconpath():
    return pkgpath() + "/pics"
    