# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proclauncher.ui'
#
# Created: Mon Apr  4 14:02:58 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcLauncher(object):
    def setupUi(self, ProcLauncher):
        ProcLauncher.setObjectName("ProcLauncher")
        ProcLauncher.resize(640, 569)
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
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cbMeasurementLabel = QtGui.QComboBox(self.centralwidget)
        self.cbMeasurementLabel.setEditable(True)
        self.cbMeasurementLabel.setObjectName("cbMeasurementLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cbMeasurementLabel)
        self.horizontalLayout.addLayout(self.formLayout)
        self.bFindExec = QtGui.QPushButton(self.centralwidget)
        self.bFindExec.setObjectName("bFindExec")
        self.horizontalLayout.addWidget(self.bFindExec)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.procLayout = QtGui.QGridLayout(self.groupBox_2)
        self.procLayout.setObjectName("procLayout")
        self.verticalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.deviceOpLayout = QtGui.QGroupBox(self.centralwidget)
        self.deviceOpLayout.setObjectName("deviceOpLayout")
        self.deviceLayout = QtGui.QGridLayout(self.deviceOpLayout)
        self.deviceLayout.setObjectName("deviceLayout")
        self.verticalLayout_2.addWidget(self.deviceOpLayout)
        ProcLauncher.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ProcLauncher)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
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
        self.actionCollect_cores = QtGui.QAction(ProcLauncher)
        self.actionCollect_cores.setObjectName("actionCollect_cores")
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionSetup_device)
        self.menuFile.addAction(self.actionCollect_cores)
        self.menubar.addAction(self.menuFile.menuAction())
        self.label.setBuddy(self.inpProcName)
        self.label_2.setBuddy(self.inpProcArgs)

        self.retranslateUi(ProcLauncher)
        QtCore.QMetaObject.connectSlotsByName(ProcLauncher)

    def retranslateUi(self, ProcLauncher):
        ProcLauncher.setWindowTitle(QtGui.QApplication.translate("ProcLauncher", "Cardinal", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ProcLauncher", "Exec", None, QtGui.QApplication.UnicodeUTF8))
        self.inpProcName.setToolTip(QtGui.QApplication.translate("ProcLauncher", "Excecutable name (e.g. /usr/bin/ls)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ProcLauncher", "Args", None, QtGui.QApplication.UnicodeUTF8))
        self.inpProcArgs.setToolTip(QtGui.QApplication.translate("ProcLauncher", "Arguments to the program", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ProcLauncher", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.cbMeasurementLabel.setToolTip(QtGui.QApplication.translate("ProcLauncher", "Label under which measurement will be filed", None, QtGui.QApplication.UnicodeUTF8))
        self.bFindExec.setText(QtGui.QApplication.translate("ProcLauncher", "Find...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ProcLauncher", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.bConnect.setText(QtGui.QApplication.translate("ProcLauncher", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("ProcLauncher", "Process launch", None, QtGui.QApplication.UnicodeUTF8))
        self.deviceOpLayout.setTitle(QtGui.QApplication.translate("ProcLauncher", "Device operations", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("ProcLauncher", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("ProcLauncher", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetup_device.setText(QtGui.QApplication.translate("ProcLauncher", "Setup device", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCollect_cores.setText(QtGui.QApplication.translate("ProcLauncher", "Collect cores", None, QtGui.QApplication.UnicodeUTF8))

