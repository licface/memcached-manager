# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Sun Oct 12 14:38:07 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,499,317).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0,26,499,268))
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.treeCluster = QtGui.QTreeWidget(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeCluster.sizePolicy().hasHeightForWidth())
        self.treeCluster.setSizePolicy(sizePolicy)
        self.treeCluster.setMinimumSize(QtCore.QSize(150,0))
        self.treeCluster.setMaximumSize(QtCore.QSize(200,16777215))
        self.treeCluster.setObjectName("treeCluster")
        self.hboxlayout.addWidget(self.treeCluster)

        self.tabsMain = QtGui.QTabWidget(self.centralwidget)
        self.tabsMain.setMinimumSize(QtCore.QSize(325,0))
        self.tabsMain.setObjectName("tabsMain")

        self.MTasks = QtGui.QWidget()
        self.MTasks.setGeometry(QtCore.QRect(0,0,321,222))
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
        self.vboxlayout.addWidget(self.gbTasks)
        self.tabsMain.addTab(self.MTasks,"")

        self.SKInfo = QtGui.QWidget()
        self.SKInfo.setGeometry(QtCore.QRect(0,0,321,222))
        self.SKInfo.setObjectName("SKInfo")
        self.tabsMain.addTab(self.SKInfo,"")

        self.Stats = QtGui.QWidget()
        self.Stats.setObjectName("Stats")
        self.tabsMain.addTab(self.Stats,"")
        self.hboxlayout.addWidget(self.tabsMain)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,499,26))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menu_Servers = QtGui.QMenu(self.menubar)
        self.menu_Servers.setObjectName("menu_Servers")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setGeometry(QtCore.QRect(0,294,499,23))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionAddServer = QtGui.QAction(MainWindow)
        self.actionAddServer.setObjectName("actionAddServer")

        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.actionAddCluster = QtGui.QAction(MainWindow)
        self.actionAddCluster.setObjectName("actionAddCluster")

        self.actionTest_Sub_Item = QtGui.QAction(MainWindow)
        self.actionTest_Sub_Item.setObjectName("actionTest_Sub_Item")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionQuit)
        self.menu_Servers.addAction(self.actionAddServer)
        self.menu_Servers.addAction(self.actionAddCluster)
        self.menu_Servers.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Servers.menuAction())

        self.retranslateUi(MainWindow)
        self.tabsMain.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.treeCluster.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Clusters", None, QtGui.QApplication.UnicodeUTF8))
        self.gbClearKey.setTitle(QtGui.QApplication.translate("MainWindow", "Delete Key(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCacheKeys.setText(QtGui.QApplication.translate("MainWindow", "Cache Key(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.txtCacheKeys.setToolTip(QtGui.QApplication.translate("MainWindow", "Seperate Keys with \';\'", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCacheKeys.setText(QtGui.QApplication.translate("MainWindow", "Delete Key(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.gbTasks.setTitle(QtGui.QApplication.translate("MainWindow", "Server Admin Tasks", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFlushCache.setToolTip(QtGui.QApplication.translate("MainWindow", "Flush Keys from All Servers in Cluster", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFlushCache.setText(QtGui.QApplication.translate("MainWindow", "Flush Cache Keys", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.MTasks), QtGui.QApplication.translate("MainWindow", "Management Tasks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsMain.setTabToolTip(self.tabsMain.indexOf(self.MTasks),QtGui.QApplication.translate("MainWindow", "Cluster Management Tasks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.SKInfo), QtGui.QApplication.translate("MainWindow", "Slab && Key Info", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsMain.setTabToolTip(self.tabsMain.indexOf(self.SKInfo),QtGui.QApplication.translate("MainWindow", "Slabs, Keys, & Values", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.Stats), QtGui.QApplication.translate("MainWindow", "Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Servers.setTitle(QtGui.QApplication.translate("MainWindow", "&Servers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddServer.setText(QtGui.QApplication.translate("MainWindow", "&Add Server", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Sa&ve", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddCluster.setText(QtGui.QApplication.translate("MainWindow", "Add &Cluster", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest_Sub_Item.setText(QtGui.QApplication.translate("MainWindow", "Test Sub Item", None, QtGui.QApplication.UnicodeUTF8))

