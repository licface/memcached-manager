# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddServer.ui'
#
# Created: Sun Nov 16 15:14:16 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_addServerDialog(object):
    def setupUi(self, addServerDialog):
        addServerDialog.setObjectName("addServerDialog")
        addServerDialog.resize(286, 185)
        self.gridLayout_2 = QtGui.QGridLayout(addServerDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lblServerIP = QtGui.QLabel(addServerDialog)
        self.lblServerIP.setObjectName("lblServerIP")
        self.gridLayout.addWidget(self.lblServerIP, 1, 0, 1, 1)
        self.txtServerIP = QtGui.QLineEdit(addServerDialog)
        self.txtServerIP.setWindowModality(QtCore.Qt.NonModal)
        self.txtServerIP.setMaxLength(15)
        self.txtServerIP.setObjectName("txtServerIP")
        self.gridLayout.addWidget(self.txtServerIP, 1, 1, 1, 1)
        self.lblServerPort = QtGui.QLabel(addServerDialog)
        self.lblServerPort.setObjectName("lblServerPort")
        self.gridLayout.addWidget(self.lblServerPort, 2, 0, 1, 1)
        self.txtServerPort = QtGui.QLineEdit(addServerDialog)
        self.txtServerPort.setObjectName("txtServerPort")
        self.gridLayout.addWidget(self.txtServerPort, 2, 1, 1, 1)
        self.lblServerName = QtGui.QLabel(addServerDialog)
        self.lblServerName.setObjectName("lblServerName")
        self.gridLayout.addWidget(self.lblServerName, 3, 0, 1, 1)
        self.txtServerName = QtGui.QLineEdit(addServerDialog)
        self.txtServerName.setObjectName("txtServerName")
        self.gridLayout.addWidget(self.txtServerName, 3, 1, 1, 1)
        self.cbCluster = QtGui.QComboBox(addServerDialog)
        self.cbCluster.setObjectName("cbCluster")
        self.gridLayout.addWidget(self.cbCluster, 0, 1, 1, 1)
        self.lblCluster = QtGui.QLabel(addServerDialog)
        self.lblCluster.setObjectName("lblCluster")
        self.gridLayout.addWidget(self.lblCluster, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnCancel = QtGui.QPushButton(addServerDialog)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.btnSave = QtGui.QPushButton(addServerDialog)
        self.btnSave.setDefault(True)
        self.btnSave.setFlat(False)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(addServerDialog)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), addServerDialog.close)
        QtCore.QMetaObject.connectSlotsByName(addServerDialog)

    def retranslateUi(self, addServerDialog):
        addServerDialog.setWindowTitle(QtGui.QApplication.translate("addServerDialog", "Add Server", None, QtGui.QApplication.UnicodeUTF8))
        self.lblServerIP.setText(QtGui.QApplication.translate("addServerDialog", "Server IP Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblServerPort.setText(QtGui.QApplication.translate("addServerDialog", "Server Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblServerName.setText(QtGui.QApplication.translate("addServerDialog", "Server Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCluster.setText(QtGui.QApplication.translate("addServerDialog", "Server Cluster", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("addServerDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("addServerDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))

