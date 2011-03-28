# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'procexplorer.ui'
#
# Created: Mon Mar 28 17:44:03 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcExplorer(object):
    def setupUi(self, ProcExplorer):
        ProcExplorer.setObjectName("ProcExplorer")
        ProcExplorer.resize(618, 401)
        self.verticalLayout = QtGui.QVBoxLayout(ProcExplorer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(ProcExplorer)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bProc = QtGui.QToolButton(ProcExplorer)
        self.bProc.setObjectName("bProc")
        self.horizontalLayout.addWidget(self.bProc)
        self.bKill = QtGui.QToolButton(ProcExplorer)
        self.bKill.setObjectName("bKill")
        self.horizontalLayout.addWidget(self.bKill)
        self.bScan = QtGui.QToolButton(ProcExplorer)
        self.bScan.setObjectName("bScan")
        self.horizontalLayout.addWidget(self.bScan)
        self.bBundle = QtGui.QToolButton(ProcExplorer)
        self.bBundle.setObjectName("bBundle")
        self.horizontalLayout.addWidget(self.bBundle)
        self.bPostProc = QtGui.QToolButton(ProcExplorer)
        self.bPostProc.setObjectName("bPostProc")
        self.horizontalLayout.addWidget(self.bPostProc)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProcExplorer)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(ProcExplorer)

    def retranslateUi(self, ProcExplorer):
        ProcExplorer.setWindowTitle(QtGui.QApplication.translate("ProcExplorer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.bProc.setText(QtGui.QApplication.translate("ProcExplorer", "proc/", None, QtGui.QApplication.UnicodeUTF8))
        self.bKill.setText(QtGui.QApplication.translate("ProcExplorer", "Kill", None, QtGui.QApplication.UnicodeUTF8))
        self.bScan.setText(QtGui.QApplication.translate("ProcExplorer", "Scn", None, QtGui.QApplication.UnicodeUTF8))
        self.bBundle.setText(QtGui.QApplication.translate("ProcExplorer", "Bundle", None, QtGui.QApplication.UnicodeUTF8))
        self.bPostProc.setText(QtGui.QApplication.translate("ProcExplorer", "Postproc", None, QtGui.QApplication.UnicodeUTF8))

