from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_MainWindow import Ui_MainWindow
from ServerActions import Dialogs
import sys
from Settings import Settings

from matplotlib import pyplot


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
        self.connect(self.btnRefresh, QtCore.SIGNAL('clicked()'), self.refreshStats)
        
        
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
            self.checkServerStatus()
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
            self.checkServerStatus()
            self.currentCluster.deleteKey(value)
            QtGui.QMessageBox.information(self, "Key(s) Deleted", "Your key(s) have been deleted")
        else:
            QtGui.QMessageBox.critical(self, "Not Cluster Selected", "You do not have an Active Cluster")
            
    def flushKeys(self):
        if self.currentCluster is not None:
            self.checkServerStatus()
            self.currentCluster.flushKeys()
            QtGui.QMessageBox.information(self, "Cache Keys Flushed", "Your keys have been flushed")
        else:
            QtGui.QMessageBox.critical(self, "Not Cluster Selected", "You do not have an Active Cluster")
            
    def mainTabChanged(self, tab):
        if tab.objectName() == 'Stats':
            self.refreshStats()
            
    def refreshStats(self):
        self.pbStats.setValue(0)
        if self.currentCluster is not None:
            self.checkServerStatus()
            stats = self.currentCluster.getStats()
            self.pbStats.setValue(1)
            
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
            
            self.pbStats.setValue(50)
            
            #Update Diagrams Tab
            #TODO: Use Temp Folder for Image storage or Figure out how to use binary string
            figure = pyplot.figure(figsize=(3,3))
            totalSpace = stats.getTotalSpace()
            freeSpace = stats.getFreeSpace()
            values = []
            labels = []
            colors = []
            for server in stats.getServers():
                colors.extend(('r','b'))
                labels.extend(("Free", "Used"))
                if(server.getFreeSpace() > 0):
                    freePerc = (float(server.getFreeSpace())/totalSpace)*100
                else:
                    freePerc = 0
                    
                if(server.getUsedSpace() > 0):
                    usedPerc = (float(server.getUsedSpace())/totalSpace)*100
                else:
                    usedPerc = 0
                    
                values.extend((freePerc, usedPerc))
            
            pie = pyplot.pie(values, labels=labels, shadow=True, autopct="%1.1f%%", colors=colors)
            pyplot.title('Cache Usage')
            figure.savefig('CacheUsage.png')
            self.lblCacheUsageGraph.setPixmap(QtGui.QPixmap('CacheUsage.png'))
            
            self.pbStats.setValue(75)
            
            figure = pyplot.figure(figsize=(3,3))
            if stats.getGets() > 0:
                hits = float(stats.getHits())/stats.getGets()*100
                misses = float(stats.getMisses())/stats.getGets()*100
            else:
                hits = 0
                misses = 0
                
            bar = pyplot.bar((0.25,1), (hits, misses), 0.5, color='r')
            pyplot.title('Hits vs. Misses')
            pyplot.gca().set_xticklabels(('Hits', 'Misses'))
            pyplot.gca().set_xticks((0.5,1.25))
            pyplot.gca().text(bar[0].get_x()+bar[0].get_width()/2.0, 1.0*bar[0].get_height(), "%1.2f%%"%(hits,), ha='center', va='bottom')
            pyplot.gca().text(bar[1].get_x()+bar[1].get_width()/2.0, 1.0*bar[1].get_height(), "%1.2f%%"%(misses,), ha='center', va='bottom')
            
            figure.savefig('HitsMisses.png')
            self.lblHitsMissesGraph.setPixmap(QtGui.QPixmap('HitsMisses.png'))
            
            self.pbStats.setValue(100)
        else:
            QtGui.QMessageBox.critical(self, "Not Cluster Selected", "You do not have an Active Cluster")
            
    def checkServerStatus(self):
        if self.currentCluster is not None:
            for server in self.currentCluster.memcached.servers:
                if server._check_dead() == 0:
                    if server.connect() == 0:
                        QtGui.QMessageBox.critical(self, "Server Disconnect", "Memcached Server "+ server.host +" Failed to Connect")

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
    sys.exit(app.exec_())
    