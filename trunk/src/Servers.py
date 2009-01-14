from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtCore import QStringList

class Server:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.menuItems = {'menu': None, 'actions':{'delete': None}}
        self.cluster = None
        self.tree = None
        
    def initTreeView(self):
        self.tree = QTreeWidgetItem(self.cluster.treeItem, QStringList(str(self.name) +" ( "+ str(self.ip) +" )"))
        
    def save(self):
        return {'name':self.name, 'ip':self.ip, 'port':self.port}
    
    def setMenuItems(self, items):
        self.menuItems = items
        
    def setCluster(self, cluster):
        self.cluster = cluster
        
    def delete(self):
        if self.menuItems['menu'] is not None:
            self.menuItems['menu'].parent().removeAction(self.menuItems['menu'].menuAction())
            
        self.cluster.deleteServer(self)