# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddCluster.ui'
#
# Created: Mon Nov 10 19:29:33 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AddClusterDialog(object):
    def setupUi(self, AddClusterDialog):
        AddClusterDialog.setObjectName("AddClusterDialog")
        AddClusterDialog.resize(257, 84)
        self.verticalLayout = QtGui.QVBoxLayout(AddClusterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lblCluster = QtGui.QLabel(AddClusterDialog)
        self.lblCluster.setObjectName("lblCluster")
        self.gridLayout.addWidget(self.lblCluster, 0, 0, 1, 1)
        self.txtClusterName = QtGui.QLineEdit(AddClusterDialog)
        self.txtClusterName.setObjectName("txtClusterName")
        self.gridLayout.addWidget(self.txtClusterName, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnCancel = QtGui.QPushButton(AddClusterDialog)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.btnSave = QtGui.QPushButton(AddClusterDialog)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AddClusterDialog)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), AddClusterDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AddClusterDialog)

    def retranslateUi(self, AddClusterDialog):
        AddClusterDialog.setWindowTitle(QtGui.QApplication.translate("AddClusterDialog", "Add Cluster", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCluster.setText(QtGui.QApplication.translate("AddClusterDialog", "Cluster Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("AddClusterDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("AddClusterDialog", "Add Cluster", None, QtGui.QApplication.UnicodeUTF8))

