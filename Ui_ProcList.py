# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proclist.ui'
#
# Created: Tue Apr  5 11:20:24 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcList(object):
    def setupUi(self, ProcList):
        ProcList.setObjectName("ProcList")
        ProcList.resize(661, 551)
        self.verticalLayout = QtGui.QVBoxLayout(ProcList)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtGui.QTableWidget(ProcList)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bRefresh = QtGui.QPushButton(ProcList)
        self.bRefresh.setObjectName("bRefresh")
        self.horizontalLayout.addWidget(self.bRefresh)
        self.bKill = QtGui.QPushButton(ProcList)
        self.bKill.setObjectName("bKill")
        self.horizontalLayout.addWidget(self.bKill)
        self.bStrace = QtGui.QPushButton(ProcList)
        self.bStrace.setObjectName("bStrace")
        self.horizontalLayout.addWidget(self.bStrace)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProcList)
        QtCore.QMetaObject.connectSlotsByName(ProcList)

    def retranslateUi(self, ProcList):
        ProcList.setWindowTitle(QtGui.QApplication.translate("ProcList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.bRefresh.setText(QtGui.QApplication.translate("ProcList", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.bKill.setText(QtGui.QApplication.translate("ProcList", "Kill", None, QtGui.QApplication.UnicodeUTF8))
        self.bStrace.setText(QtGui.QApplication.translate("ProcList", "strace", None, QtGui.QApplication.UnicodeUTF8))

