class Cluster:
    def __init__(self, name):
        self.servers = []
        self.name = name
        
    def addServer(self, server):
        self.servers.append(server)
        
    def save(self):
        save = {'name':self.name, 'servers':[]}
        for server in self.servers:
            save['servers'].append(server.save())
            
        return save