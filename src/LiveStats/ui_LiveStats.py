# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LiveStats.ui'
#
# Created: Thu Nov 20 01:18:56 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_liveStatsDialog(object):
    def setupUi(self, liveStatsDialog):
        liveStatsDialog.setObjectName("liveStatsDialog")
        liveStatsDialog.resize(650, 453)
        self.verticalLayout = QtGui.QVBoxLayout(liveStatsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(liveStatsDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 628, 395))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gbConnections = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbConnections.setObjectName("gbConnections")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbConnections)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblConnectionsGraph = QtGui.QLabel(self.gbConnections)
        self.lblConnectionsGraph.setObjectName("lblConnectionsGraph")
        self.verticalLayout_3.addWidget(self.lblConnectionsGraph)
        self.verticalLayout_4.addWidget(self.gbConnections)
        self.gbGetsSets = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbGetsSets.setObjectName("gbGetsSets")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.gbGetsSets)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblGetsGraph = QtGui.QLabel(self.gbGetsSets)
        self.lblGetsGraph.setObjectName("lblGetsGraph")
        self.verticalLayout_5.addWidget(self.lblGetsGraph)
        self.verticalLayout_4.addWidget(self.gbGetsSets)
        self.gbHitsMisses = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbHitsMisses.setObjectName("gbHitsMisses")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.gbHitsMisses)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lblHitsMissesGraph = QtGui.QLabel(self.gbHitsMisses)
        self.lblHitsMissesGraph.setObjectName("lblHitsMissesGraph")
        self.verticalLayout_7.addWidget(self.lblHitsMissesGraph)
        self.verticalLayout_4.addWidget(self.gbHitsMisses)
        self.gbMemoryUsage = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbMemoryUsage.setObjectName("gbMemoryUsage")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbMemoryUsage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblMemoryUsage = QtGui.QLabel(self.gbMemoryUsage)
        self.lblMemoryUsage.setObjectName("lblMemoryUsage")
        self.verticalLayout_2.addWidget(self.lblMemoryUsage)
        self.verticalLayout_4.addWidget(self.gbMemoryUsage)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblIntervalTxt = QtGui.QLabel(liveStatsDialog)
        self.lblIntervalTxt.setObjectName("lblIntervalTxt")
        self.horizontalLayout.addWidget(self.lblIntervalTxt)
        self.txtInterval = QtGui.QLineEdit(liveStatsDialog)
        self.txtInterval.setObjectName("txtInterval")
        self.horizontalLayout.addWidget(self.txtInterval)
        self.btnStartStop = QtGui.QPushButton(liveStatsDialog)
        self.btnStartStop.setObjectName("btnStartStop")
        self.horizontalLayout.addWidget(self.btnStartStop)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(liveStatsDialog)
        QtCore.QMetaObject.connectSlotsByName(liveStatsDialog)

    def retranslateUi(self, liveStatsDialog):
        liveStatsDialog.setWindowTitle(QtGui.QApplication.translate("liveStatsDialog", "Live Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.gbConnections.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Active Connections", None, QtGui.QApplication.UnicodeUTF8))
        self.lblConnectionsGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Active Connections Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.gbGetsSets.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Gets && Sets", None, QtGui.QApplication.UnicodeUTF8))
        self.lblGetsGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Gets & Sets Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.gbHitsMisses.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Hits vs. Misses", None, QtGui.QApplication.UnicodeUTF8))
        self.lblHitsMissesGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Hits vs. Misses Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.gbMemoryUsage.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Memory Usage", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMemoryUsage.setText(QtGui.QApplication.translate("liveStatsDialog", "Memory Usage Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.lblIntervalTxt.setText(QtGui.QApplication.translate("liveStatsDialog", "Refresh Interval:", None, QtGui.QApplication.UnicodeUTF8))
        self.txtInterval.setText(QtGui.QApplication.translate("liveStatsDialog", "30", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStartStop.setText(QtGui.QApplication.translate("liveStatsDialog", "Start/Stop", None, QtGui.QApplication.UnicodeUTF8))

