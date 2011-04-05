#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import madre

import Ui_Beamer
import os, re

class Beamer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Beamer.Ui_Beamer()
        self.ui.setupUi(self)

