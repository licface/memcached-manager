from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_MainWindow import Ui_MainWindow
from ServerActions import Dialogs
import sys
from Settings import Settings

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.addServerDialog = Dialogs.AddServer()
        self.addClusterDialog = Dialogs.AddCluster()
        self.settings = Settings()
        
        self.connect(self.actionAddServer, QtCore.SIGNAL("triggered()"), self.displayAddServer)
        self.connect(self.actionAddCluster, QtCore.SIGNAL("triggered()"), self.displayAddCluster)
        self.connect(self.addServerDialog, QtCore.SIGNAL('saved'), self.addServer)
        self.connect(self.addClusterDialog, QtCore.SIGNAL('saved'), self.addCluster)
        self.addServerDialog.connect(self.addClusterDialog, QtCore.SIGNAL('saved'), self.addServerDialog.addCluster)
        self.connect(self.actionSave, QtCore.SIGNAL('triggered()'), self.save)
        
        for cluster in self.settings.servers.getClusters():
            self.addCluster(cluster)
    
    def displayAddCluster(self):
        self.addServerDialog.hide()
        self.addClusterDialog.show()
        
    def displayAddServer(self):
        self.addClusterDialog.hide()
        self.addServerDialog.show()
        self.addServerDialog.updateClusters()
        
    def save(self):
        self.settings.save()
        
    def addCluster(self, cluster):
        items = cluster.menuItems
        items['menu'] = self.menu_Servers.addMenu(cluster.name)
        items['actions']['delete'] = QtGui.QAction(self)
        items['actions']['delete'].setText('Delete')
        items['menu'].addAction(items['actions']['delete'])
        items['menu'].addSeparator()
        items['servers'] = items['menu'].addMenu('Servers')
        items['actions']['add'] = QtGui.QAction(self)
        items['actions']['add'].setText('Add Server')
        items['servers'].addAction(items['actions']['add'])
        items['servers'].addSeparator()
        self.connect(items['actions']['add'], QtCore.SIGNAL("triggered()"), self.displayAddServer)
        self.connect(items['actions']['delete'], QtCore.SIGNAL("triggered()"), self.deleteCluster)
        
        cluster.setMenuItems(items)
        
        for server in cluster.getServers():
            self.addServer(cluster, server)
            
    def deleteCluster(self):
        action = self.sender()
        cluster = self.settings.servers.getClusterByMenuItem(action)
        if cluster is not None:
            self.settings.servers.deleteCluster(cluster)
            
        
    def addServer(self, cluster, server):
        items = server.menuItems
        items['menu'] = cluster.menuItems['servers'].addMenu(server.name)
        items['actions']['delete'] = QtGui.QAction(self)
        items['actions']['delete'].setText('Delete')
        items['menu'].addAction(items['actions']['delete'])
        
        

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
    sys.exit(app.exec_())
    