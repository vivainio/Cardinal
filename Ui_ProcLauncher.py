# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proclauncher.ui'
#
# Created: Wed Mar 23 12:14:12 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcLauncher(object):
    def setupUi(self, ProcLauncher):
        ProcLauncher.setObjectName("ProcLauncher")
        ProcLauncher.resize(849, 792)
        self.centralwidget = QtGui.QWidget(ProcLauncher)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.inpProcName = QtGui.QLineEdit(self.centralwidget)
        self.inpProcName.setObjectName("inpProcName")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.inpProcName)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.inpProcArgs = QtGui.QLineEdit(self.centralwidget)
        self.inpProcArgs.setObjectName("inpProcArgs")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.inpProcArgs)
        self.horizontalLayout.addLayout(self.formLayout)
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.bConnect = QtGui.QPushButton(self.groupBox)
        self.bConnect.setGeometry(QtCore.QRect(230, 0, 101, 27))
        self.bConnect.setObjectName("bConnect")
        self.cbHost = QtGui.QComboBox(self.groupBox)
        self.cbHost.setGeometry(QtCore.QRect(94, 0, 111, 27))
        self.cbHost.setEditable(True)
        self.cbHost.setObjectName("cbHost")
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.bLaRun = QtGui.QPushButton(self.centralwidget)
        self.bLaRun.setObjectName("bLaRun")
        self.verticalLayout.addWidget(self.bLaRun)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.deviceOpLayout = QtGui.QGridLayout()
        self.deviceOpLayout.setObjectName("deviceOpLayout")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.deviceOpLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.deviceOpLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.deviceOpLayout)
        ProcLauncher.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ProcLauncher)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 849, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        ProcLauncher.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ProcLauncher)
        self.statusbar.setObjectName("statusbar")
        ProcLauncher.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(ProcLauncher)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSetup_device = QtGui.QAction(ProcLauncher)
        self.actionSetup_device.setObjectName("actionSetup_device")
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionSetup_device)
        self.menubar.addAction(self.menuFile.menuAction())
        self.label.setBuddy(self.inpProcName)
        self.label_2.setBuddy(self.inpProcArgs)

        self.retranslateUi(ProcLauncher)
        QtCore.QMetaObject.connectSlotsByName(ProcLauncher)

    def retranslateUi(self, ProcLauncher):
        ProcLauncher.setWindowTitle(QtGui.QApplication.translate("ProcLauncher", "Cardinal", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ProcLauncher", "Exec", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ProcLauncher", "Args", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("ProcLauncher", "Find...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ProcLauncher", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.bConnect.setText(QtGui.QApplication.translate("ProcLauncher", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.bLaRun.setText(QtGui.QApplication.translate("ProcLauncher", "Ping", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("ProcLauncher", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("ProcLauncher", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("ProcLauncher", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("ProcLauncher", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetup_device.setText(QtGui.QApplication.translate("ProcLauncher", "Setup device", None, QtGui.QApplication.UnicodeUTF8))

