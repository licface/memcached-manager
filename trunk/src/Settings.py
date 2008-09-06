from configobj import ConfigObj
import os
import sys
from Clusters import Cluster
from Servers import Server

class Settings:
    settings = None
    servers = None
    
    def __init__(self):
        if self.settings is None:
            self.settings = GlobalSettings()
        
        if self.servers is None:
            self.servers = ServerSettings()

class GlobalSettings:
    __settings = {}
    
    def __init__(self):
        self.__dict__ = self.__settings

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
                self.config = ConfigObj()
                self.config.filename = self.configPath
                self.config['clusters'] = []
                self.config.write()
            else:
                self.config = ConfigObj(self.configPath)
            
    def loadClusters(self):
        if not self.__dict__.has_key('clusters') or self.clusters is None:
            self.clusters = []
            for cluster in self.config['clusters']:
                tCluster = Cluster(self.config['clusters'][cluster]['name'])
                for server in self.config['clusters'][cluster]['servers']:
                    tServer = Server(
                                     self.config['clusters'][cluster]['servers'][server]['name'],
                                     self.config['clusters'][cluster]['servers'][server]['ip'],
                                     self.config['clusters'][cluster]['servers'][server]['port']
                                     )
                    tCluster.addServer(tServer)
                self.clusters.append(tCluster)
            
    def save(self):
        self.config['clusters'] = []
        for cluster in self.clusters:
            self.config['clusters'].append(cluster.save())
            
        self.config.write()
        
    def getClusters(self):
        return self.clusters
    
    def getServers(self, cluster):
        pass
    
    def getAllServers(self):
        pass
    
    def addCluster(self, cluster):
        pass
    
    def addServer(self, cluster, name, ip, port):
        pass