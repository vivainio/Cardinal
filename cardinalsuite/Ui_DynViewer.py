# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dynviewer.ui'
#
# Created: Thu Apr 21 09:22:29 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DynViewer(object):
    def setupUi(self, DynViewer):
        DynViewer.setObjectName("DynViewer")
        DynViewer.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(DynViewer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bBack = QtGui.QToolButton(DynViewer)
        self.bBack.setObjectName("bBack")
        self.horizontalLayout.addWidget(self.bBack)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QtGui.QTextBrowser(DynViewer)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(DynViewer)
        QtCore.QMetaObject.connectSlotsByName(DynViewer)

    def retranslateUi(self, DynViewer):
        DynViewer.setWindowTitle(QtGui.QApplication.translate("DynViewer", "DynViewer - Cardinal", None, QtGui.QApplication.UnicodeUTF8))
        self.bBack.setText(QtGui.QApplication.translate("DynViewer", "Back", None, QtGui.QApplication.UnicodeUTF8))

