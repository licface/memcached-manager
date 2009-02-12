# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Preferences.ui'
#
# Created: Wed Feb 11 21:25:32 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PrefWindow(object):
    def setupUi(self, PrefWindow):
        PrefWindow.setObjectName("PrefWindow")
        PrefWindow.resize(422, 300)
        self.verticalLayout = QtGui.QVBoxLayout(PrefWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tbMain = QtGui.QTabWidget(PrefWindow)
        self.tbMain.setObjectName("tbMain")
        self.GraphTab = QtGui.QWidget()
        self.GraphTab.setObjectName("GraphTab")
        self.horizontalLayout = QtGui.QHBoxLayout(self.GraphTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblPieGraphColors = QtGui.QLabel(self.GraphTab)
        self.lblPieGraphColors.setObjectName("lblPieGraphColors")
        self.verticalLayout_2.addWidget(self.lblPieGraphColors)
        self.txtPieColors = QtGui.QTextEdit(self.GraphTab)
        self.txtPieColors.setObjectName("txtPieColors")
        self.verticalLayout_2.addWidget(self.txtPieColors)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblHitMissesColor = QtGui.QLabel(self.GraphTab)
        self.lblHitMissesColor.setObjectName("lblHitMissesColor")
        self.verticalLayout_3.addWidget(self.lblHitMissesColor)
        self.txtHitMissesColor = QtGui.QLineEdit(self.GraphTab)
        self.txtHitMissesColor.setMinimumSize(QtCore.QSize(100, 0))
        self.txtHitMissesColor.setObjectName("txtHitMissesColor")
        self.verticalLayout_3.addWidget(self.txtHitMissesColor)
        self.lblGetsSetsColor = QtGui.QLabel(self.GraphTab)
        self.lblGetsSetsColor.setObjectName("lblGetsSetsColor")
        self.verticalLayout_3.addWidget(self.lblGetsSetsColor)
        self.txtGetsSetsColor = QtGui.QLineEdit(self.GraphTab)
        self.txtGetsSetsColor.setMinimumSize(QtCore.QSize(100, 0))
        self.txtGetsSetsColor.setObjectName("txtGetsSetsColor")
        self.verticalLayout_3.addWidget(self.txtGetsSetsColor)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.tbMain.addTab(self.GraphTab, "")
        self.StatsTB = QtGui.QWidget()
        self.StatsTB.setObjectName("StatsTB")
        self.tbMain.addTab(self.StatsTB, "")
        self.verticalLayout.addWidget(self.tbMain)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnCancel = QtGui.QPushButton(PrefWindow)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.btnSave = QtGui.QPushButton(PrefWindow)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(PrefWindow)
        self.tbMain.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), PrefWindow.close)
        QtCore.QMetaObject.connectSlotsByName(PrefWindow)

    def retranslateUi(self, PrefWindow):
        PrefWindow.setWindowTitle(QtGui.QApplication.translate("PrefWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPieGraphColors.setText(QtGui.QApplication.translate("PrefWindow", "Pie Graph Colors:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblHitMissesColor.setText(QtGui.QApplication.translate("PrefWindow", "Hit & Misses Color:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblGetsSetsColor.setText(QtGui.QApplication.translate("PrefWindow", "Gets & Sets Color:", None, QtGui.QApplication.UnicodeUTF8))
        self.tbMain.setTabText(self.tbMain.indexOf(self.GraphTab), QtGui.QApplication.translate("PrefWindow", "Graphs", None, QtGui.QApplication.UnicodeUTF8))
        self.tbMain.setTabText(self.tbMain.indexOf(self.StatsTB), QtGui.QApplication.translate("PrefWindow", "Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("PrefWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("PrefWindow", "Save Settings", None, QtGui.QApplication.UnicodeUTF8))

