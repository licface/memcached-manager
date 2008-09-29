import md5

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
        
    def setMenuItems(self, items):
        self.menuItems = items
        
    def addServer(self, server):
        self.servers.append(server)
        server.setCluster(self)
        
    def deleteServer(self, server):
        self.servers.remove(server)
        
    def getServers(self):
        return self.servers
        
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