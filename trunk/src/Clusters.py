import md5
import memcached.memcache
import memcached.Stats
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtCore import QStringList

class Cluster:
	def __init__(self, name):
		self.servers = []
		self.name = name
		self.treeItem = None
		self.treeItemParent = None
		self.key = md5.new(self.name).hexdigest()
		
	def initTreeView(self, parent):
		self.treeItemParent = parent
		self.treeItem = QTreeWidgetItem(parent, QStringList(self.name))
		for server in self.getServers():
			server.initTreeView()
		
	def addServer(self, server):
		self.servers.append(server)
		server.setCluster(self)
		if self.treeItem is not None:
			server.initTreeView()
		
	def deleteServer(self, server):
		self.servers.remove(server)
		
	def getServers(self):
		return self.servers
	
	def getServerMemcachedUrls(self):
		servers = []
		for server in self.servers:
			servers.append(str(server.ip) +":"+ str(server.port))
		return servers
		
	def save(self):
		save = {'name':self.name, 'servers':[]}
		for server in self.servers:
			save['servers'].append(server.save())
			
		return save
	
	def delete(self):			
		for server in self.servers:
			server.delete()
		self.servers = []
			
		if self.treeItemParent is not None and self.treeItem is not None:
			self.treeItemParent.removeItemWidget(self.treeItem, 0)
				
	def getMemcached(self):
		return memcached.memcache.Client(self.getServerMemcachedUrls(), debug=0)
			
	#Memcached Management Functions
			
	def deleteKey(self, key):
		keys = key.split(';')
		mc = self.getMemcached()
		mc.delete_multi(keys)
		mc.disconnect_all()
		
	def flushKeys(self):
		mc = self.getMemcached()
		mc.flush_all()
		mc.disconnect_all()
		
	def getStats(self):
		mc = self.getMemcached()
		stats = memcached.Stats.MemcachedStats(mc.get_stats())
		mc.disconnect_all()
		return stats