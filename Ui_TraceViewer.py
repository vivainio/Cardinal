# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'traceviewer.ui'
#
# Created: Tue Apr  5 11:20:24 2011
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
        self.bExternal = QtGui.QToolButton(TraceViewer)
        self.bExternal.setObjectName("bExternal")
        self.verticalLayout.addWidget(self.bExternal)
        self.bFollow = QtGui.QToolButton(TraceViewer)
        self.bFollow.setCheckable(True)
        self.bFollow.setObjectName("bFollow")
        self.verticalLayout.addWidget(self.bFollow)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(TraceViewer)
        QtCore.QMetaObject.connectSlotsByName(TraceViewer)

    def retranslateUi(self, TraceViewer):
        TraceViewer.setWindowTitle(QtGui.QApplication.translate("TraceViewer", "TraceViewer", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setToolTip(QtGui.QApplication.translate("TraceViewer", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("TraceViewer", "R", None, QtGui.QApplication.UnicodeUTF8))
        self.bExternal.setText(QtGui.QApplication.translate("TraceViewer", "E", None, QtGui.QApplication.UnicodeUTF8))
        self.bFollow.setToolTip(QtGui.QApplication.translate("TraceViewer", "Follow", None, QtGui.QApplication.UnicodeUTF8))
        self.bFollow.setText(QtGui.QApplication.translate("TraceViewer", "F", None, QtGui.QApplication.UnicodeUTF8))

