# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'procexplorer.ui'
#
# Created: Wed Mar 23 15:33:48 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcExplorer(object):
    def setupUi(self, ProcExplorer):
        ProcExplorer.setObjectName("ProcExplorer")
        ProcExplorer.resize(503, 582)
        self.verticalLayout = QtGui.QVBoxLayout(ProcExplorer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(ProcExplorer)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(ProcExplorer)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProcExplorer)

    def retranslateUi(self, ProcExplorer):
        ProcExplorer.setWindowTitle(QtGui.QApplication.translate("ProcExplorer", "Form", None, QtGui.QApplication.UnicodeUTF8))

