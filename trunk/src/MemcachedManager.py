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
from Dialogs import Preferences, Add
import sys
from Settings import Settings

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
		self.ManagementTasks = ManagementTasks.ManagementTasks(self)
		self.Slabs = Slabs.Slabs(self)
		self.Stats = Stats.Stats(self)
		
		self.addDialog = Add.AddServersClusters()
		self.preferencesDialog = Preferences.Preferences()
		self.settings = Settings()
		
		self.connect(self.actionAddClusterServer, QtCore.SIGNAL("triggered()"), self.displayAdd)
		self.connect(self.btnAddClusterServer, QtCore.SIGNAL("clicked()"), self.displayAdd)
		self.connect(self.addDialog, QtCore.SIGNAL('savedServer'), self.addServer)
		self.connect(self.addDialog, QtCore.SIGNAL('savedCluster'), self.addCluster)
		
		self.connect(self.actionSave, QtCore.SIGNAL('triggered()'), self.save)
		self.connect(self.actionPreferences, QtCore.SIGNAL('triggered()'), self.displayPreferences)
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
		"""
		Signal Capture for when the Main set of tabs change.
		
		This is used to cann an onFocus even for each tab 
		allowing them to update data if needed or preferances saying to. 
		"""
		if tab.objectName() == 'Stats':
			self.Stats.onFocus()
		elif tab.objectName() == 'SKInfo':
			self.Slabs.onFocus()
		elif tab.objectName() == 'MTasks':
			self.ManagementTasks.onFocus()

	def displayTreeContextMenu(self, point):
		"""
		Starts of the context menu for the Tree
		"""
		#self.treeCluster.indexAt(point)
		self.treeCMServer.popup(QtGui.QCursor.pos())
	
	def displayAdd(self):
		"""
		Displays the Add Server/Cluster Dialog when the Signal 
		is emited from Buttons or Actions.
		"""
		self.addDialog.show()
		
	def displayPreferences(self):
		"""
		Displays the Preferences Dialog when the Signal is 
		emited from Buttons or Actions.
		"""
		self.preferencesDialog.show()
		
	def save(self):
		"""
		Saves your Preferences and Servers/Clusters.
		"""
		self.settings.save()
		
	def addCluster(self, cluster):
		"""
		Adds a Cluster to the Tree View and Menu System.
		"""
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
		
		self.connect(items['actions']['add'], QtCore.SIGNAL("triggered()"), self.displayAdd)
		self.connect(items['actions']['delete'], QtCore.SIGNAL("triggered()"), self.deleteCluster)
		self.connect(items['actions']['set'], QtCore.SIGNAL("triggered()"), self.setCluster)
		
		cluster.setMenuItems(items)
		
		for server in cluster.getServers():
			self.addServer(cluster, server)
		
		cluster.initTreeView(self.treeCluster)
			
	def deleteCluster(self):
		"""
		Deletes a Cluster and its Servers from the Tree View and Menu
		"""
		action = self.sender()
		cluster = self.settings.servers.getClusterByMenuItem(action)
		if cluster is not None:
			self.settings.servers.deleteCluster(cluster)
			
		self.addDialog.updateClusters()
		self.settings.servers.save()
			
	def setCluster(self):
		"""
		Sets the Current Active Cluster when a signal is emited from the Menu
		"""
		action = self.sender()
		cluster = self.settings.servers.getClusterByMenuItem(action)
		if cluster is not None:
			self.makeClusterActive(cluster)
			
	def setClusterByTree(self, treeItem, column, *args, **kargs):
		"""
		Sets the Current Active Cluster when a signal is emited from the Tree View
		"""
		for cluster in self.settings.servers.getClusters():
			if cluster.treeItem == treeItem:
				self.makeClusterActive(cluster)
			
	def makeClusterActive(self, cluster):
		"""
		Sets the Current Active Cluster and updates the title of the window to reflex this.
		"""
		self.currentCluster = cluster
		self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Memcached Manager ("+ str(self.currentCluster.name) +")", None, QtGui.QApplication.UnicodeUTF8))
		
	def addServer(self, cluster, server):
		"""
		Adds a Server to a Cluster in the Tree View and Menu
		"""
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
		"""
		Delete a Server from the Menu and Tree View
		"""
		action = self.sender()
		server = self.settings.servers.getServerByMenuItem(action)
		server.delete()
		self.settings.servers.save()
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
	sys.exit(app.exec_())
	
