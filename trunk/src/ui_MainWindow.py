# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Sat Sep  6 13:38:39 2008
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
        self.centralwidget.setGeometry(QtCore.QRect(170,26,422,375))
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tbMain = QtGui.QToolBox(self.centralwidget)
        self.tbMain.setFrameShape(QtGui.QFrame.Panel)
        self.tbMain.setObjectName("tbMain")

        self.MTasks = QtGui.QWidget()
        self.MTasks.setGeometry(QtCore.QRect(0,0,402,259))
        self.MTasks.setObjectName("MTasks")

        self.vboxlayout = QtGui.QVBoxLayout(self.MTasks)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gbClearKey = QtGui.QGroupBox(self.MTasks)
        self.gbClearKey.setFlat(False)
        self.gbClearKey.setObjectName("gbClearKey")

        self.gridlayout = QtGui.QGridLayout(self.gbClearKey)
        self.gridlayout.setObjectName("gridlayout")

        self.lblCacheKeys = QtGui.QLabel(self.gbClearKey)
        self.lblCacheKeys.setObjectName("lblCacheKeys")
        self.gridlayout.addWidget(self.lblCacheKeys,0,0,1,1)

        self.txtCacheKeys = QtGui.QLineEdit(self.gbClearKey)
        self.txtCacheKeys.setObjectName("txtCacheKeys")
        self.gridlayout.addWidget(self.txtCacheKeys,0,1,1,1)

        self.btnCacheKeys = QtGui.QPushButton(self.gbClearKey)
        self.btnCacheKeys.setObjectName("btnCacheKeys")
        self.gridlayout.addWidget(self.btnCacheKeys,1,1,1,1)
        self.vboxlayout.addWidget(self.gbClearKey)

        self.gbTasks = QtGui.QGroupBox(self.MTasks)
        self.gbTasks.setObjectName("gbTasks")

        self.gridlayout1 = QtGui.QGridLayout(self.gbTasks)
        self.gridlayout1.setObjectName("gridlayout1")

        self.btnFlushCache = QtGui.QPushButton(self.gbTasks)
        self.btnFlushCache.setObjectName("btnFlushCache")
        self.gridlayout1.addWidget(self.btnFlushCache,0,0,1,1)

        self.btnRestart = QtGui.QPushButton(self.gbTasks)
        self.btnRestart.setObjectName("btnRestart")
        self.gridlayout1.addWidget(self.btnRestart,0,1,1,1)
        self.vboxlayout.addWidget(self.gbTasks)
        self.tbMain.addItem(self.MTasks,"")

        self.SlabsKeys = QtGui.QWidget()
        self.SlabsKeys.setGeometry(QtCore.QRect(0,0,402,259))
        self.SlabsKeys.setObjectName("SlabsKeys")
        self.tbMain.addItem(self.SlabsKeys,"")

        self.Stats = QtGui.QWidget()
        self.Stats.setObjectName("Stats")
        self.tbMain.addItem(self.Stats,"")
        self.hboxlayout.addWidget(self.tbMain)
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
        self.serverDock.setGeometry(QtCore.QRect(0,26,164,375))
        self.serverDock.setObjectName("serverDock")

        self.dockWidgetContents_2 = QtGui.QWidget(self.serverDock)
        self.dockWidgetContents_2.setGeometry(QtCore.QRect(0,23,164,352))
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.dockWidgetContents_2)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.serverTree = QtGui.QTreeView(self.dockWidgetContents_2)
        self.serverTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.serverTree.setFrameShape(QtGui.QFrame.StyledPanel)
        self.serverTree.setFrameShadow(QtGui.QFrame.Sunken)
        self.serverTree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.serverTree.setObjectName("serverTree")
        self.hboxlayout1.addWidget(self.serverTree)
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
        self.tbMain.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.gbClearKey.setTitle(QtGui.QApplication.translate("MainWindow", "Delete Key(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCacheKeys.setText(QtGui.QApplication.translate("MainWindow", "Cache Key(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCacheKeys.setText(QtGui.QApplication.translate("MainWindow", "Delete Key(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.gbTasks.setTitle(QtGui.QApplication.translate("MainWindow", "Server Admin Tasks", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFlushCache.setText(QtGui.QApplication.translate("MainWindow", "Flush All Cache Keys", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRestart.setText(QtGui.QApplication.translate("MainWindow", "Restart Server", None, QtGui.QApplication.UnicodeUTF8))
        self.tbMain.setItemText(self.tbMain.indexOf(self.MTasks), QtGui.QApplication.translate("MainWindow", "Managment Tasks", None, QtGui.QApplication.UnicodeUTF8))
        self.tbMain.setItemText(self.tbMain.indexOf(self.SlabsKeys), QtGui.QApplication.translate("MainWindow", "Slabs && Keys", None, QtGui.QApplication.UnicodeUTF8))
        self.tbMain.setItemText(self.tbMain.indexOf(self.Stats), QtGui.QApplication.translate("MainWindow", "Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Servers.setTitle(QtGui.QApplication.translate("MainWindow", "&Servers", None, QtGui.QApplication.UnicodeUTF8))
        self.serverDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Servers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddServer.setText(QtGui.QApplication.translate("MainWindow", "&Add Server", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Sa&ve", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))

