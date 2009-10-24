#!/usr/bin/env python
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

Copyright
=========

Copyright (C) 2008,2009  Nick Verbeck <nerdynick@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import matplotlib
matplotlib.use('QT4Agg')
from PyQt4 import QtGui
from PyQt4 import QtCore
from Tabs import ManagementTasks, Slabs, Stats
from ui_MainWindow import Ui_MainWindow
from Dialogs import Preferences, Add, About
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
		self.aboutDialog = About.About()
		
		self.settings = Settings()
		
		self.connect(self, QtCore.SIGNAL('destroyed(QObject*)'), self.closeAll)
		
		self.connect(self.actionAddClusterServer, QtCore.SIGNAL("triggered()"), self.displayAdd)
		self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.displayAbout)
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
		self.treeCMServerActions['deleteServer'].setText("Delete")
		self.treeCMServer.addAction(self.treeCMServerActions['deleteServer'])
		self.connect(self.treeCMServerActions['deleteServer'], QtCore.SIGNAL("triggered()"), self.deleteServer)


		self.treeCMCluster = QtGui.QMenu()
		self.treeCMClusterActions = {"deleteCluster": QtGui.QAction(self), "makeActive": QtGui.QAction(self)}
		self.treeCMClusterActions['deleteCluster'].setText("Delete")
		self.treeCMCluster.addAction(self.treeCMClusterActions['deleteCluster'])
		self.treeCMClusterActions['makeActive'].setText("Make Active")
		self.treeCMCluster.addAction(self.treeCMClusterActions['makeActive'])
		self.connect(self.treeCMClusterActions['deleteCluster'], QtCore.SIGNAL("triggered()"), self.deleteCluster)
		self.connect(self.treeCMClusterActions['makeActive'], QtCore.SIGNAL("triggered()"), self.setClusterByContextMenu)
			
	def displayAbout(self):
		self.aboutDialog.show()
	
	def closeAll(self, *args, **kargs):
		print 'Closing'
		self.Stats.onClose()
		self.Slabs.onClose()
		self.ManagementTasks.onClose()
		
		self.addDialog.close()
		self.preferencesDialog.close()
		
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
		#print self.treeCluster.indexAt(point)
		found = False
		for cluster in self.settings.servers.getClusters():
			if cluster.treeItem == self.treeCluster.currentItem():
				self.treeCMCluster.popup(QtGui.QCursor.pos())
				found = True
				break
		if found is False:
			for server in self.settings.servers.getAllServers():
				if server.tree == self.treeCluster.currentItem():
					self.treeCMServer.popup(QtGui.QCursor.pos())
					break
	
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
		Adds a Cluster to the Tree View.
		"""
		cluster.initTreeView(self.treeCluster)
			
	def deleteCluster(self):
		"""
		Deletes a Cluster and its Servers from the Tree View and Menu
		"""
		for cluster in self.settings.servers.getClusters():
			if cluster.treeItem == self.treeCluster.currentItem():
				self.settings.servers.deleteCluster(cluster)
				self.addDialog.updateClusters()
				self.settings.servers.save()
				break
			
	def setClusterByTree(self, treeItem, column, *args, **kargs):
		"""
		Sets the Current Active Cluster when a signal is emited from the Tree View
		"""
		for cluster in self.settings.servers.getClusters():
			if cluster.treeItem == treeItem:
				self.makeClusterActive(cluster)
				break
		
	def setClusterByContextMenu(self):
		for cluster in self.settings.servers.getClusters():
			if cluster.treeItem == self.treeCluster.currentItem():
				self.makeClusterActive(cluster)
				break
			
	def makeClusterActive(self, cluster):
		"""
		Sets the Current Active Cluster and updates the title of the window to reflex this.
		"""
		self.currentCluster = cluster
		self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Memcached Manager ("+ str(self.currentCluster.name) +")", None, QtGui.QApplication.UnicodeUTF8))

		
	def deleteServer(self):
		"""
		Delete a Server from the Tree
		"""
		for server in self.settings.servers.getAllServers():
			if server.tree == self.treeCluster.currentItem():
				server.delete()
				self.settings.servers.save()
				break
		
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
	sys.exit(app.exec_())
	
