import md5
import memcached.memcache
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtCore import QStringList

class Cluster:
    def __init__(self, name):
        self.servers = []
        self.name = name
        self.menuItems = {
                 'menu':None, 
                 'servers':None, 
                 'actions':{
                            'delete':None, 
                            'add':None,
                            'set':None
                            }
                 }
        
        self.treeItem = None
        
        self.key = md5.new(self.name).hexdigest()
        
        self.memcached = memcached.memcache.Client(self.getServerMemcachedUrls(), debug=0)
        
    def initTreeView(self, parent):
        self.treeItem = QTreeWidgetItem(parent, QStringList(self.name))
        for server in self.getServers():
            server.initTreeView()
        
    def setMenuItems(self, items):
        self.menuItems = items
        
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
            
        if self.menuItems['menu'] is not None:
            self.menuItems['menu'].parent().removeAction(self.menuItems['menu'].menuAction())
            
    #Memcached Management Functions
            
    def deleteKey(self, key):
        keys = key.split(';')
        self.memcached.delete_multi(keys)
        
    def flushKeys(self):
        self.memcached.flush_all()