# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logviewer.ui'
#
# Created: Thu Apr 21 09:22:30 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LogViewer(object):
    def setupUi(self, LogViewer):
        LogViewer.setObjectName("LogViewer")
        LogViewer.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(LogViewer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.teLog = QtGui.QPlainTextEdit(LogViewer)
        self.teLog.setObjectName("teLog")
        self.verticalLayout.addWidget(self.teLog)

        self.retranslateUi(LogViewer)
        QtCore.QMetaObject.connectSlotsByName(LogViewer)

    def retranslateUi(self, LogViewer):
        LogViewer.setWindowTitle(QtGui.QApplication.translate("LogViewer", "LogViewer", None, QtGui.QApplication.UnicodeUTF8))

