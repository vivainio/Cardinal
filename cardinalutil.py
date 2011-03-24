#!/usr/bin/env python

from PyQt4 import QtCore, QtGui


def cachedir():
    cloc = str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.CacheLocation)).rstrip("/")
    return cloc + "/cardinal"