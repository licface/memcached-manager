from PyQt4 import QtCore
from PyQt4 import QtGui

class ManagementTasks:
	def __init__(self, mainWindow):
		self.mainWindow = mainWindow
		
		self.mainWindow.connect(self.mainWindow.btnDelCacheKeys, QtCore.SIGNAL("clicked()"), self.deleteKeys)
		self.mainWindow.connect(self.mainWindow.btnGetCacheKeys, QtCore.SIGNAL("clicked()"), self.getKeys)
		self.mainWindow.connect(self.mainWindow.btnFlushCache, QtCore.SIGNAL("clicked()"), self.flushServers)
		self.mainWindow.connect(self.mainWindow.btnKeySearch, QtCore.SIGNAL("clicked()"), self.keySearch)
		
	def onFocus(self):
		"""
		Event called by MemcachedManager when this tab gains focus
		"""
		pass
	
	def onClose(self):
		pass
	
	def getKeys(self):
		value = self.mainWindow.txtCacheKeys.text()
		if self.mainWindow.currentCluster is not None:
			self.mainWindow.cachedItemDialog.hide()
			self.mainWindow.cachedItemDialog.show()
			self.mainWindow.cachedItemDialog.setCluster(self.mainWindow.currentCluster)
			self.mainWindow.cachedItemDialog.setKeys(value)
		else:
			QtGui.QMessageBox.critical(self.mainWindow, "Not Cluster Selected", "You do not have an Active Cluster")
		
	def deleteKeys(self):
		"""
		Deletes a key(s) from the Current Active Cluster 
		"""
		value = self.mainWindow.txtCacheKeys.text()
		if self.mainWindow.currentCluster is not None:
			self.mainWindow.currentCluster.deleteKey(value)
			QtGui.QMessageBox.information(self.mainWindow, "Key(s) Deleted", "Your key(s) have been deleted")
		else:
			QtGui.QMessageBox.critical(self.mainWindow, "Not Cluster Selected", "You do not have an Active Cluster")
	
	def flushServers(self):
		"""
		Flush all Keys from the Current Active Cluster
		"""
		if self.mainWindow.currentCluster is not None:
			self.mainWindow.currentCluster.flushKeys()
			QtGui.QMessageBox.information(self.mainWindow, "Cache Keys Flushed", "Your keys have been flushed")
		else:
			QtGui.QMessageBox.critical(self.mainWindow, "Not Cluster Selected", "You do not have an Active Cluster")
	
	def keySearch(self):
		"""
		Preform a Key Search
		
		This is still under development
		"""
		#pBar = pbKeySearch
		#RegEx = cbRegEx
		#Text = txtSearchKey
		QtGui.QMessageBox.information(self.mainWindow, "Key Search", "Key Search is currently under development.")