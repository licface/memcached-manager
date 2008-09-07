from PyQt4 import QtCore
from PyQt4 import Qt

class Server:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        
    def save(self):
        return {'name':self.name, 'ip':self.ip, 'port':self.port}
    
class ServerTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.rootItem = ServerTreeItem('Clusters')
        
    def index(self, row, column, parent):
        pass
    
    def parent(self, index):
        pass
    
    def rowCount(self, parent):
        pass
    
    def columnCount(self, parent):
        pass
    
    def data(self, index, role):
        pass
    
    def flags(self, index):
        pass
    
    def headerData(self, section, orientation, role):
        pass

        
class ServerTreeItem():
    def __init__(self, data, parent=None):
        self.itemData = data
        self.parentItem = parent
        self.childItems = []
        
    def appendChild(self, child):
        self.childItems.append(child)
        
    def child(self, row):
        pass
    
    def childCount(self):
        return len(self.childItems)
    
    def row(self):
        pass
    
    def columnCount(self):
        pass
    
    def data(self, column):
        return self.itemData
    
    def parent(self):
        return self.parentItem