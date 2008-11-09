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
        self.connect(self.tabsMain, QtCore.SIGNAL('currentChanged(QWidget*)'), self.mainTabChanged)
        
        #Management Task Actions
        self.connect(self.btnCacheKeys, QtCore.SIGNAL("clicked()"), self.deleteKeys)
        self.connect(self.btnFlushCache, QtCore.SIGNAL("clicked()"), self.flushKeys)
        
        self.currentCluster = None
        
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
        items['actions']['set'] = QtGui.QAction(self)
        items['actions']['set'].setText('Make Active')
        items['menu'].addAction(items['actions']['set'])
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
        self.connect(items['actions']['set'], QtCore.SIGNAL("triggered()"), self.setCluster)
        
        cluster.setMenuItems(items)
        
        for server in cluster.getServers():
            self.addServer(cluster, server)
        
        cluster.initTreeView(self.treeCluster)
            
    def deleteCluster(self):
        action = self.sender()
        cluster = self.settings.servers.getClusterByMenuItem(action)
        if cluster is not None:
            self.settings.servers.deleteCluster(cluster)
            
    def setCluster(self):
        action = self.sender()
        self.currentCluster = self.settings.servers.getClusterByMenuItem(action)
        if self.currentCluster is not None:
            self.currentCluster.makeActive()
            self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow ("+ str(self.currentCluster.name) +")", None, QtGui.QApplication.UnicodeUTF8))
            
        
    def addServer(self, cluster, server):
        items = server.menuItems
        items['menu'] = cluster.menuItems['servers'].addMenu(server.name)
        items['actions']['delete'] = QtGui.QAction(self)
        items['actions']['delete'].setText('Delete')
        items['menu'].addAction(items['actions']['delete'])
        self.connect(items['actions']['delete'], QtCore.SIGNAL("triggered()"), self.deleteServer)
        
    def deleteServer(self):
        action = self.sender()
        server = self.settings.servers.getServerByMenuItem(action)
        server.delete()
        
    def deleteKeys(self):
        value = self.txtCacheKeys.text()
        if self.currentCluster is not None:
            self.currentCluster.deleteKey(value)
            QtGui.QMessageBox.information(self, "Key(s) Deleted", "Your key(s) have been deleted")
        else:
            QtGui.QMessageBox.critical(self, "Not Cluster Selected", "You do not have an Active Cluster")
            
    def flushKeys(self):
        if self.currentCluster is not None:
            self.currentCluster.flushKeys()
            QtGui.QMessageBox.information(self, "Cache Keys Flushed", "Your keys have been flushed")
        else:
            QtGui.QMessageBox.critical(self, "Not Cluster Selected", "You do not have an Active Cluster")
            
    def mainTabChanged(self, tab):
        if tab.objectName() == 'Stats':
            self.refreshStats()
            
    def refreshStats(self):
        if self.currentCluster is not None:
            stats = self.currentCluster.getStats()
            
            #Update Cache Info Tab
            self.lblItems.setText(str(stats.getTotalItems()))
            self.lblCurrentItems.setText(str(stats.getItems()))
            self.lblConnections.setText(str(stats.getTotalConnections()))
            self.lblCurrentConnections.setText(str(stats.getConnections()))
            self.lblHits.setText(str(stats.getHits()))
            self.lblMisses.setText(str(stats.getMisses()))
            self.lblGets.setText(str(stats.getGets()))
            self.lblSets.setText(str(stats.getSets()))
            self.lblSpace.setText(str(stats.getTotalSpace()))
            self.lblFree.setText(str(stats.getFreeSpace()))
            self.lblUsed.setText(str(stats.getUsedSpace()))
            self.lblRequestRate.setText("%.2f cache requests/second"% (stats.getRequestRate(),))
            self.lblHitRate.setText("%.2f cache requests/second"% (stats.getHitRate(),))
            self.lblMissRate.setText("%.2f cache requests/second"% (stats.getMissRate(),))
            self.lblSetRate.setText("%.2f cache requests/second"% (stats.getSetRate(),))
        else:
            QtGui.QMessageBox.critical(self, "Not Cluster Selected", "You do not have an Active Cluster")
        
            
        

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
    sys.exit(app.exec_())
    