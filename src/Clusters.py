import md5
import memcached.memcache

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
        self.key = md5.new(self.name).hexdigest()
        
        self.memcached = memcached.memcache.Client(self.getServerMemcachedUrls(), debug=0)
        
    def setMenuItems(self, items):
        self.menuItems = items
        
    def addServer(self, server):
        self.servers.append(server)
        server.setCluster(self)
        
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
            
    def deleteKey(self, key):
        keys = key.split(';')
        self.memcached.delete_multi(keys)