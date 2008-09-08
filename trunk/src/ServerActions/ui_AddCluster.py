# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddCluster.ui'
#
# Created: Sun Sep  7 16:21:45 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AddClusterDialog(object):
    def setupUi(self, AddClusterDialog):
        AddClusterDialog.setObjectName("AddClusterDialog")
        AddClusterDialog.resize(QtCore.QSize(QtCore.QRect(0,0,257,84).size()).expandedTo(AddClusterDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(AddClusterDialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.lblCluster = QtGui.QLabel(AddClusterDialog)
        self.lblCluster.setObjectName("lblCluster")
        self.gridlayout.addWidget(self.lblCluster,0,0,1,1)

        self.txtClusterName = QtGui.QLineEdit(AddClusterDialog)
        self.txtClusterName.setObjectName("txtClusterName")
        self.gridlayout.addWidget(self.txtClusterName,0,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.btnCancel = QtGui.QPushButton(AddClusterDialog)
        self.btnCancel.setObjectName("btnCancel")
        self.hboxlayout.addWidget(self.btnCancel)

        self.btnSave = QtGui.QPushButton(AddClusterDialog)
        self.btnSave.setObjectName("btnSave")
        self.hboxlayout.addWidget(self.btnSave)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(AddClusterDialog)
        QtCore.QObject.connect(self.btnCancel,QtCore.SIGNAL("clicked()"),AddClusterDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AddClusterDialog)

    def retranslateUi(self, AddClusterDialog):
        AddClusterDialog.setWindowTitle(QtGui.QApplication.translate("AddClusterDialog", "Add Cluster", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCluster.setText(QtGui.QApplication.translate("AddClusterDialog", "Cluster Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("AddClusterDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("AddClusterDialog", "Add Cluster", None, QtGui.QApplication.UnicodeUTF8))

