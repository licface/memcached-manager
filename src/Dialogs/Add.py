from PyQt4 import QtGui
from PyQt4 import QtCore
from Dialogs.ui_Add import Ui_AddDialog
from Settings import Settings
from Clusters import Cluster

class AddServersClusters(QtGui.QDialog, Ui_AddDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		self.settings = Settings()
		self.updateClusters()
		
		self.connect(self.btnAddCluster, QtCore.SIGNAL('clicked()'), self.saveCluster)
		self.connect(self.btnAddServer, QtCore.SIGNAL('clicked()'), self.saveServer)
		
	def saveCluster(self):
		cluster = Cluster(self.txtClusterName.text())
		self.settings.servers.addCluster(cluster)
		self.cbClusters.addItem(self.txtClusterName.text())
		self.settings.servers.save()
		
		self.txtClusterName.setText('')
		self.emit(QtCore.SIGNAL('savedCluster'), cluster)
	
	def saveServer(self):
		cluster = self.settings.servers.getCluster(self.cbClusters.currentText())
		address = self.txtServerAddress.text()
		port = self.txtServerPort.text()
		name = self.txtServerName.text()
		
		server = self.settings.servers.addServer(cluster, name, address, port)
		self.settings.servers.save()
		
		self.txtServerAddress.setText('')
		self.txtServerPort.setText('')
		self.txtServerName.setText('')
		
		self.emit(QtCore.SIGNAL('savedServer'), cluster, server)
		
	def updateClusters(self):
		self.cbClusters.clear()
		clusters = self.settings.servers.getClusters()
		for cluster in clusters:
			self.cbClusters.addItem(cluster.name)