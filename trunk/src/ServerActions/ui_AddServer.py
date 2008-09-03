# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddServer.ui'
#
# Created: Sat Aug 30 19:37:41 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_addServerDialog(object):
    def setupUi(self, addServerDialog):
        addServerDialog.setObjectName("addServerDialog")
        addServerDialog.resize(QtCore.QSize(QtCore.QRect(0,0,286,152).size()).expandedTo(addServerDialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(addServerDialog)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.lblServerIP = QtGui.QLabel(addServerDialog)
        self.lblServerIP.setObjectName("lblServerIP")
        self.gridlayout1.addWidget(self.lblServerIP,0,0,1,1)

        self.txtServerIP = QtGui.QLineEdit(addServerDialog)
        self.txtServerIP.setWindowModality(QtCore.Qt.NonModal)
        self.txtServerIP.setMaxLength(15)
        self.txtServerIP.setObjectName("txtServerIP")
        self.gridlayout1.addWidget(self.txtServerIP,0,1,1,1)

        self.lblServerPort = QtGui.QLabel(addServerDialog)
        self.lblServerPort.setObjectName("lblServerPort")
        self.gridlayout1.addWidget(self.lblServerPort,1,0,1,1)

        self.txtServerPort = QtGui.QLineEdit(addServerDialog)
        self.txtServerPort.setObjectName("txtServerPort")
        self.gridlayout1.addWidget(self.txtServerPort,1,1,1,1)

        self.lblServerName = QtGui.QLabel(addServerDialog)
        self.lblServerName.setObjectName("lblServerName")
        self.gridlayout1.addWidget(self.lblServerName,2,0,1,1)

        self.txtServerName = QtGui.QLineEdit(addServerDialog)
        self.txtServerName.setObjectName("txtServerName")
        self.gridlayout1.addWidget(self.txtServerName,2,1,1,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.btnCancel = QtGui.QPushButton(addServerDialog)
        self.btnCancel.setObjectName("btnCancel")
        self.hboxlayout.addWidget(self.btnCancel)

        self.btnSave = QtGui.QPushButton(addServerDialog)
        self.btnSave.setDefault(True)
        self.btnSave.setFlat(False)
        self.btnSave.setObjectName("btnSave")
        self.hboxlayout.addWidget(self.btnSave)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,1)

        self.retranslateUi(addServerDialog)
        QtCore.QObject.connect(self.btnCancel,QtCore.SIGNAL("clicked()"),addServerDialog.close)
        QtCore.QMetaObject.connectSlotsByName(addServerDialog)

    def retranslateUi(self, addServerDialog):
        addServerDialog.setWindowTitle(QtGui.QApplication.translate("addServerDialog", "Add Server", None, QtGui.QApplication.UnicodeUTF8))
        self.lblServerIP.setText(QtGui.QApplication.translate("addServerDialog", "Server IP Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblServerPort.setText(QtGui.QApplication.translate("addServerDialog", "Server Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblServerName.setText(QtGui.QApplication.translate("addServerDialog", "Server Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("addServerDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("addServerDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))

