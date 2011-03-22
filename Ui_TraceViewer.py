# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'traceviewer.ui'
#
# Created: Tue Mar 22 10:38:09 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TraceViewer(object):
    def setupUi(self, TraceViewer):
        TraceViewer.setObjectName("TraceViewer")
        TraceViewer.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(TraceViewer)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtGui.QPlainTextEdit(TraceViewer)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnRefresh = QtGui.QToolButton(TraceViewer)
        self.btnRefresh.setObjectName("btnRefresh")
        self.verticalLayout.addWidget(self.btnRefresh)
        self.toolButton_2 = QtGui.QToolButton(TraceViewer)
        self.toolButton_2.setObjectName("toolButton_2")
        self.verticalLayout.addWidget(self.toolButton_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(TraceViewer)
        QtCore.QMetaObject.connectSlotsByName(TraceViewer)

    def retranslateUi(self, TraceViewer):
        TraceViewer.setWindowTitle(QtGui.QApplication.translate("TraceViewer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setToolTip(QtGui.QApplication.translate("TraceViewer", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("TraceViewer", "R", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("TraceViewer", "E", None, QtGui.QApplication.UnicodeUTF8))

