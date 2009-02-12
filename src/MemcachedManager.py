"""
Memcached Server Manager

Overview
========

Memcached Manager is a very simple yet powerful memcached server/cluster manager. 
It allows you to delete & flush keys, view stats, see the raw data on the server, and more. 

Author
======

U{Nick "NerdyNick" Verbeck   <nerdynick@gmail.com>}

Version
=======

0.1

Detailed Documentation
======================

You can read more documentation at U{http://code.google.com/p/memcached-manager/}
"""

from PyQt4 import QtGui
from PyQt4 import QtCore
from Tabs import ManagementTasks, Slabs, Stats
from ui_MainWindow import Ui_MainWindow
from Dialogs import AddServer, AddCluster
import sys
from Settings import Settings

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.ManagementTasks = ManagementTasks.ManagementTasks(self)
		self.Slabs = Slabs.Slabs(self)
		self.Stats = Stats.Stats(self)
		
		self.addServerDialog = AddServer.AddServer()
		self.addClusterDialog = AddCluster.AddCluster()
		self.settings = Settings()
		
		self.connect(self.actionAddServer, QtCore.SIGNAL("triggered()"), self.displayAddServer)
		self.connect(self.actionAddCluster, QtCore.SIGNAL("triggered()"), self.displayAddCluster)
		self.connect(self.btnAddServer, QtCore.SIGNAL("clicked()"), self.displayAddServer)
		self.connect(self.btnAddCluster, QtCore.SIGNAL("clicked()"), self.displayAddCluster)
		self.connect(self.addServerDialog, QtCore.SIGNAL('saved'), self.addServer)
		self.connect(self.addClusterDialog, QtCore.SIGNAL('saved'), self.addCluster)
		
		self.addServerDialog.connect(self.addClusterDialog, QtCore.SIGNAL('saved'), self.addServerDialog.addCluster)
		self.connect(self.actionSave, QtCore.SIGNAL('triggered()'), self.save)
		self.connect(self.tabsMain, QtCore.SIGNAL('currentChanged(QWidget*)'), self.mainTabChanged)
		
		self.treeCluster.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.treeCluster, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.setClusterByTree)
		self.connect(self.treeCluster, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.displayTreeContextMenu)
		
		self.currentCluster = None
		
		for cluster in self.settings.servers.getClusters():
			self.addCluster(cluster)
			
		
		self.treeCMServer = QtGui.QMenu()
		self.treeCMServerActions = {"deleteServer": QtGui.QAction(self)}
		self.treeCMServerActions['deleteServer'].setText("Delete Server")
		self.treeCMServer.addAction(self.treeCMServerActions['deleteServer'])


		self.treeCMCluster = QtGui.QMenu()
		self.treeCMClusterActions = {"deleteCluster": QtGui.QAction(self), "makeActive": QtGui.QAction(self)}
		self.treeCMClusterActions['deleteCluster'].setText("Delete Cluster")
		self.treeCMCluster.addAction(self.treeCMClusterActions['deleteCluster'])
		self.treeCMClusterActions['makeActive'].setText("Make Active")
		self.treeCMCluster.addAction(self.treeCMClusterActions['makeActive'])
			
	def mainTabChanged(self, tab):
		if tab.objectName() == 'Stats':
			self.Stats.onFocus()
		elif tab.objectName() == 'SKInfo':
			self.Slabs.onFocus()
		elif tab.objectName() == 'MTasks':
			self.ManagementTasks.onFocus()

	def displayTreeContextMenu(self, point):
		#self.treeCluster.indexAt(point)
		self.treeCMServer.popup(QtGui.QCursor.pos())
	
	def displayAddCluster(self):
		self.addServerDialog.hide()
		self.addClusterDialog.show()
		
	def displayAddServer(self):
		self.addClusterDialog.hide()
		self.addServerDialog.show()
		self.addServerDialog.updateClusters()
		
	def save(self):
		self.settings.save()
		
	def addCluster(self, cluster):
		items = cluster.menuItems
		items['menu'] = self.menu_Servers.addMenu(cluster.name)
		items['actions']['set'] = QtGui.QAction(self)
		items['actions']['set'].setText('Make Active')
		ActiveIcon = QtGui.QIcon()
		ActiveIcon.addPixmap(QtGui.QPixmap("Icons/Active.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		items['actions']['set'].setIcon(ActiveIcon)
		
		items['menu'].addAction(items['actions']['set'])
		items['actions']['delete'] = QtGui.QAction(self)
		items['actions']['delete'].setText('Delete')
		RemoveIcon = QtGui.QIcon()
		RemoveIcon.addPixmap(QtGui.QPixmap("Icons/Remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		items['actions']['delete'].setIcon(RemoveIcon)
		
		items['menu'].addAction(items['actions']['delete'])
		items['menu'].addSeparator()
		items['servers'] = items['menu'].addMenu('Servers')
		items['actions']['add'] = QtGui.QAction(self)
		items['actions']['add'].setText('Add Server')
		AddIcon = QtGui.QIcon()
		AddIcon.addPixmap(QtGui.QPixmap("Icons/Add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		items['actions']['add'].setIcon(AddIcon)
		
		items['servers'].addAction(items['actions']['add'])
		items['servers'].addSeparator()
		
		self.connect(items['actions']['add'], QtCore.SIGNAL("triggered()"), self.displayAddServer)
		self.connect(items['actions']['delete'], QtCore.SIGNAL("triggered()"), self.deleteCluster)
		self.connect(items['actions']['set'], QtCore.SIGNAL("triggered()"), self.setCluster)
		
		cluster.setMenuItems(items)
		
		for server in cluster.getServers():
			self.addServer(cluster, server)
		
		cluster.initTreeView(self.treeCluster)
			
	def deleteCluster(self):
		action = self.sender()
		cluster = self.settings.servers.getClusterByMenuItem(action)
		if cluster is not None:
			self.settings.servers.deleteCluster(cluster)
			
	def setCluster(self):
		action = self.sender()
		cluster = self.settings.servers.getClusterByMenuItem(action)
		if cluster is not None:
			self.makeClusterActive(cluster)
			
	def setClusterByTree(self, treeItem, column, *args, **kargs):
		for cluster in self.settings.servers.getClusters():
			if cluster.treeItem == treeItem:
				self.makeClusterActive(cluster)
			
	def makeClusterActive(self, cluster):
		self.currentCluster = cluster
		self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Memcached Manager ("+ str(self.currentCluster.name) +")", None, QtGui.QApplication.UnicodeUTF8))
		
	def addServer(self, cluster, server):
		items = server.menuItems
		items['menu'] = cluster.menuItems['servers'].addMenu(server.name)
		items['actions']['delete'] = QtGui.QAction(self)
		items['actions']['delete'].setText('Delete')
		RemoveIcon = QtGui.QIcon()
		RemoveIcon.addPixmap(QtGui.QPixmap("Icons/Remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		items['actions']['delete'].setIcon(RemoveIcon)
		items['menu'].addAction(items['actions']['delete'])
		self.connect(items['actions']['delete'], QtCore.SIGNAL("triggered()"), self.deleteServer)
		
	def deleteServer(self):
		action = self.sender()
		server = self.settings.servers.getServerByMenuItem(action)
		server.delete()
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
	sys.exit(app.exec_())
	
