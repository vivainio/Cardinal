# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beamer.ui'
#
# Created: Thu Apr 21 09:05:28 2011
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
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.bFetchOutbox = QtGui.QPushButton(Beamer)
        self.bFetchOutbox.setObjectName("bFetchOutbox")
        self.gridLayout.addWidget(self.bFetchOutbox, 0, 0, 1, 1)
        self.bDropClipboard = QtGui.QPushButton(Beamer)
        self.bDropClipboard.setObjectName("bDropClipboard")
        self.gridLayout.addWidget(self.bDropClipboard, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Beamer)
        QtCore.QMetaObject.connectSlotsByName(Beamer)

    def retranslateUi(self, Beamer):
        Beamer.setWindowTitle(QtGui.QApplication.translate("Beamer", "Beamer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Beamer", "Push to inbox by dropping files here", None, QtGui.QApplication.UnicodeUTF8))
        self.bFetchOutbox.setText(QtGui.QApplication.translate("Beamer", "Fetch outbox", None, QtGui.QApplication.UnicodeUTF8))
        self.bDropClipboard.setText(QtGui.QApplication.translate("Beamer", "Drop from clipboard", None, QtGui.QApplication.UnicodeUTF8))

