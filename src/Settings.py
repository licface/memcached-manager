import os
import sys
from Clusters import Cluster
from Servers import Server
import pickle

class Settings:
    settings = None
    servers = None
    
    def __init__(self):
        if self.settings is None:
            self.settings = GlobalSettings()
        
        if self.servers is None:
            self.servers = ServerSettings()
            
    def save(self):
        self.settings.save()
        self.servers.save()

class GlobalSettings:
    __settings = {}
    
    def __init__(self):
        self.__dict__ = self.__settings
        
    def save(self):
        pass

class ServerSettings:
    __settings = {}
    
    def __init__(self):
        self.__dict__ = self.__settings
        self.loadConfig()
        self.loadClusters()
        
    def __del__(self):
        self.save()
            
    def loadConfig(self):
        if not self.__dict__.has_key('configPath') or self.configPath is None:
            self.configPath = os.path.join(sys.path[0], 'servers.ini')
            
        if not self.__dict__.has_key('config') or self.config is None:
            if os.path.exists(self.configPath) is not True:
                self.config = {'clusters': []}
            else:
                self.config = pickle.load(open(self.configPath, 'rb'))
            
    def loadClusters(self):
        if not self.__dict__.has_key('clusters') or self.clusters is None:
            self.clusters = []
            for cluster in self.config['clusters']:
                tCluster = Cluster(cluster['name'])
                for server in cluster['servers']:
                    tServer = Server(
                                     server['name'],
                                     server['ip'],
                                     server['port']
                                     )
                    tCluster.addServer(tServer)
                self.clusters.append(tCluster)
                
            if len(self.clusters) <= 0:
                self.addDefaults()
        
    def addDefaults(self):
        tCluster = Cluster('Default Cluster')
        tServer = Server('Demo Server', '127.0.0.1', '11211')
        tCluster.addServer(tServer)
        self.addCluster(tCluster)
            
    def save(self):
        self.config['clusters'] = []
        for cluster in self.clusters:
            self.config['clusters'].append(cluster.save())
            
        pickle.dump(self.config, open(self.configPath, 'wb'))
        
    def getClusters(self):
        return self.clusters
    
    def getCluster(self, name):
        for cluster in self.clusters:
            if cluster.name == name:
                return cluster
        return None
            
    def getClusterByMenuItem(self, action):
        for cluster in self.settings.servers.getClusters():
            if cluster.menuItems['actions']['delete'] == action:
                return cluster
        return None
    
    def getServers(self, cluster):
        pass
    
    def getAllServers(self):
        pass
    
    def getLength(self):
        return len(self.clusters)
    
    def addCluster(self, cluster):
        self.clusters.append(cluster)
        self.save()
        
    def deleteCluster(self, cluster):
        index = self.clusters.index(cluster)
        cluster.delete()
        self.clusters.pop(index)
    
    def addServer(self, cluster, name, ip, port):
        server = Server(name, ip, port)
        cluster.addServer(server)
        self.save()
        return server