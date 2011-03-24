# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'procexplorer.ui'
#
# Created: Thu Mar 24 19:07:47 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcExplorer(object):
    def setupUi(self, ProcExplorer):
        ProcExplorer.setObjectName("ProcExplorer")
        ProcExplorer.resize(638, 628)
        self.verticalLayout = QtGui.QVBoxLayout(ProcExplorer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(ProcExplorer)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton_4 = QtGui.QToolButton(ProcExplorer)
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout.addWidget(self.toolButton_4)
        self.toolButton = QtGui.QToolButton(ProcExplorer)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.toolButton_2 = QtGui.QToolButton(ProcExplorer)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout.addWidget(self.toolButton_2)
        self.toolButton_3 = QtGui.QToolButton(ProcExplorer)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout.addWidget(self.toolButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProcExplorer)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(ProcExplorer)

    def retranslateUi(self, ProcExplorer):
        ProcExplorer.setWindowTitle(QtGui.QApplication.translate("ProcExplorer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_4.setText(QtGui.QApplication.translate("ProcExplorer", "proc/", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("ProcExplorer", "Kill", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("ProcExplorer", "Scn", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_3.setText(QtGui.QApplication.translate("ProcExplorer", "Bundle", None, QtGui.QApplication.UnicodeUTF8))

