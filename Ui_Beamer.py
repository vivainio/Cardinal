# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beamer.ui'
#
# Created: Tue Apr  5 11:20:24 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Beamer(object):
    def setupUi(self, Beamer):
        Beamer.setObjectName("Beamer")
        Beamer.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Beamer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Beamer)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(Beamer)
        QtCore.QMetaObject.connectSlotsByName(Beamer)

    def retranslateUi(self, Beamer):
        Beamer.setWindowTitle(QtGui.QApplication.translate("Beamer", "Beamer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Beamer", "Drop files here", None, QtGui.QApplication.UnicodeUTF8))
