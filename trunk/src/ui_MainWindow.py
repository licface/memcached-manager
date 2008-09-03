# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Sat Aug 30 20:07:36 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,592,424).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(137,26,455,375))
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,592,26))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menu_Servers = QtGui.QMenu(self.menubar)
        self.menu_Servers.setObjectName("menu_Servers")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setGeometry(QtCore.QRect(0,401,592,23))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.serverDock = QtGui.QDockWidget(MainWindow)
        self.serverDock.setGeometry(QtCore.QRect(0,26,131,375))
        self.serverDock.setObjectName("serverDock")

        self.dockWidgetContents_2 = QtGui.QWidget(self.serverDock)
        self.dockWidgetContents_2.setGeometry(QtCore.QRect(0,23,131,352))
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")

        self.hboxlayout = QtGui.QHBoxLayout(self.dockWidgetContents_2)
        self.hboxlayout.setObjectName("hboxlayout")

        self.serverTree = QtGui.QTreeView(self.dockWidgetContents_2)
        self.serverTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.serverTree.setFrameShape(QtGui.QFrame.StyledPanel)
        self.serverTree.setFrameShadow(QtGui.QFrame.Sunken)
        self.serverTree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.serverTree.setObjectName("serverTree")
        self.hboxlayout.addWidget(self.serverTree)
        self.serverDock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1),self.serverDock)

        self.actionAddServer = QtGui.QAction(MainWindow)
        self.actionAddServer.setObjectName("actionAddServer")

        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionQuit)
        self.menu_Servers.addAction(self.actionAddServer)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Servers.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionQuit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Servers.setTitle(QtGui.QApplication.translate("MainWindow", "&Servers", None, QtGui.QApplication.UnicodeUTF8))
        self.serverDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Servers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddServer.setText(QtGui.QApplication.translate("MainWindow", "&Add Server", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Sa&ve", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))

