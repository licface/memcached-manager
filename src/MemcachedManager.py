"""
Memcached Server Manager

Overview
========

Memcached Manager is a very simple yet powerful memcached server/cluster manager. 
It allows you to delete & flush keys, view stats, see the raw data on the server, and more. 

Author
======

U{Nick "NerdyNick" Verbeck   <nerdynick@gmail.com>}

Version
=======

0.1

Detailed Documentation
======================

You can read more documentation at U{http://code.google.com/p/memcached-manager/}
"""

from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_MainWindow import Ui_MainWindow
from ServerActions import Dialogs
from LiveStats import LiveStatsDialog
import sys
import datetime
from Settings import Settings

from matplotlib import pyplot


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.addServerDialog = Dialogs.AddServer()
        self.addClusterDialog = Dialogs.AddCluster()
        self.liveStatsDialog = LiveStatsDialog.Dialog()
        self.settings = Settings()
        
        self.connect(self.actionAddServer, QtCore.SIGNAL("triggered()"), self.displayAddServer)
        self.connect(self.actionAddCluster, QtCore.SIGNAL("triggered()"), self.displayAddCluster)
        self.connect(self.btnAddServer, QtCore.SIGNAL("clicked()"), self.displayAddServer)
        self.connect(self.btnAddCluster, QtCore.SIGNAL("clicked()"), self.displayAddCluster)
        self.connect(self.addServerDialog, QtCore.SIGNAL('saved'), self.addServer)
        self.connect(self.addClusterDialog, QtCore.SIGNAL('saved'), self.addCluster)
        
        self.addServerDialog.connect(self.addClusterDialog, QtCore.SIGNAL('saved'), self.addServerDialog.addCluster)
        self.connect(self.actionSave, QtCore.SIGNAL('triggered()'), self.save)
        self.connect(self.tabsMain, QtCore.SIGNAL('currentChanged(QWidget*)'), self.mainTabChanged)
        self.connect(self.btnRefresh, QtCore.SIGNAL('clicked()'), self.refreshStats)
        
        
        #Management Task Actions
        self.connect(self.btnCacheKeys, QtCore.SIGNAL("clicked()"), self.deleteKeys)
        self.connect(self.btnFlushCache, QtCore.SIGNAL("clicked()"), self.flushKeys)
        
        #Stats Actions
        self.connect(self.btnWatch, QtCore.SIGNAL("clicked()"), self.watchLiveStats)
        
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
            self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Memcached Manager ("+ str(self.currentCluster.name) +")", None, QtGui.QApplication.UnicodeUTF8))
            
        
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
        elif tab.objectName() == 'SKInfo':
            self.refreshSlabsKeys()
    
    def refreshSlabsKeys(self):
        pass
            
    def refreshStats(self):
        self.pbStats.setValue(0)
        if self.currentCluster is not None:
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
            
            tSpace = stats.getSpaceString(stats.getTotalSpace())
            self.lblSpace.setText(tSpace)
            
            fSpace = stats.getSpaceString(stats.getFreeSpace())
            self.lblFree.setText(fSpace)
            
            uSpace = stats.getSpaceString(stats.getUsedSpace())
            self.lblUsed.setText(uSpace)
            
            self.lblRequestRate.setText("%.2f cache requests/second"% (stats.getRequestRate(),))
            self.lblHitRate.setText("%.2f cache requests/second"% (stats.getHitRate(),))
            self.lblMissRate.setText("%.2f cache requests/second"% (stats.getMissRate(),))
            self.lblSetRate.setText("%.2f cache requests/second"% (stats.getSetRate(),))
            self.lblGetRate.setText("%.2f cache requests/second"% (stats.getGetRate(),))
            
            self.lblRequestRateAvg.setText("%.2f cache requests/second"% (stats.getRequestRateAvg(),))
            self.lblHitRateAvg.setText("%.2f cache requests/second"% (stats.getHitRateAvg(),))
            self.lblMissRateAvg.setText("%.2f cache requests/second"% (stats.getMissRateAvg(),))
            self.lblSetRateAvg.setText("%.2f cache requests/second"% (stats.getSetRateAvg(),))
            self.lblGetRateAvg.setText("%.2f cache requests/second"% (stats.getGetRateAvg(),))
            
            self.pbStats.setValue(25)
            
            #Update Diagrams Tab
            #TODO: Use Temp Folder for Image storage or Figure out how to use binary string
            
            #Cache Usage Graph
            figure = pyplot.figure(figsize=(3,3), facecolor='#D4CCBA', edgecolor='#AB9675', dpi=100)
            totalSpace = stats.getTotalSpace()
            freeSpace = stats.getFreeSpace()
            values = []
            labels = []
            colors = []
            for server in stats.getServers():
                colors.extend(('#FFE0C9','#CF8442'))
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
            
            pyplot.pie(values, labels=labels, shadow=True, autopct="%1.1f%%", colors=colors)
            
            pyplot.title('Cache Usage')
            figure.savefig('CacheUsage.png')
            self.lblCacheUsageGraph.setPixmap(QtGui.QPixmap('CacheUsage.png'))
            
            self.pbStats.setValue(50)
            
            #Hits vs. Misses Graph
            figure = pyplot.figure(figsize=(3,3), facecolor='#D4CCBA', edgecolor='#AB9675')
            if (stats.getHits() + stats.getMisses()) > 0:
                hits = float(stats.getHits())/(stats.getHits() + stats.getMisses())*100
                misses = float(stats.getMisses())/(stats.getHits() + stats.getMisses())*100
            else:
                hits = 0
                misses = 0
                
            bar = pyplot.bar((0.25,1), (hits, misses), 0.5, color='#CF8442')
            pyplot.title('Hits vs. Misses')
            pyplot.gca().set_xticklabels(('Hits', 'Misses'))
            pyplot.gca().set_xticks((0.5,1.25))
            pyplot.gca().text(bar[0].get_x()+bar[0].get_width()/2.0, 1.0*bar[0].get_height(), "%1.2f%%"%(hits,), ha='center', va='bottom')
            pyplot.gca().text(bar[1].get_x()+bar[1].get_width()/2.0, 1.0*bar[1].get_height(), "%1.2f%%"%(misses,), ha='center', va='bottom')
            
            figure.savefig('HitsMisses.png')
            self.lblHitsMissesGraph.setPixmap(QtGui.QPixmap('HitsMisses.png'))
            
            self.pbStats.setValue(75)
            
            #Gets & Sets Graph
            figure = pyplot.figure(figsize=(3,3), facecolor='#D4CCBA', edgecolor='#AB9675')
            if (stats.getGets() + stats.getSets()) > 0:
                gets = float(stats.getGets())/(stats.getGets() + stats.getSets())*100
                sets = float(stats.getSets())/(stats.getGets() + stats.getSets())*100
            else:
                gets = 0
                sets = 0
                
            bar = pyplot.bar((0.25,1), (gets, sets), 0.5, color='#CF8442')
            pyplot.title('Gets & Sets')
            pyplot.gca().set_xticklabels(('Gets', 'Sets'))
            pyplot.gca().set_xticks((0.5,1.25))
            pyplot.gca().text(bar[0].get_x()+bar[0].get_width()/2.0, 1.0*bar[0].get_height(), "%1.2f%%"%(gets,), ha='center', va='bottom')
            pyplot.gca().text(bar[1].get_x()+bar[1].get_width()/2.0, 1.0*bar[1].get_height(), "%1.2f%%"%(sets,), ha='center', va='bottom')
            
            figure.savefig('GetsSets.png')
            self.lblGetSetGraph.setPixmap(QtGui.QPixmap('GetsSets.png'))
            
            self.pbStats.setValue(100)
            
            #Destroy the Scroll Area
            self.horizontalLayout_6.removeWidget(self.saServerInfo)
            QtCore.Qt.WA_DeleteOnClose
            self.saServerInfo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.saServerInfo.close()
            
            #Rebuild the Scroll Area
            self.saServerInfo = QtGui.QScrollArea(self.ServerInfo)
            self.saServerInfo.setWidgetResizable(True)
            self.saServerInfo.setObjectName("saServerInfo")
            self.scrollAreaWidgetContents_3 = QtGui.QWidget(self.saServerInfo)
            self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 262, 436))
            self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
            self.verticalLayout_6 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_3)
            self.verticalLayout_6.setObjectName("verticalLayout_6")
            
            #Add each server
            for s in stats.servers:
                hostStr = s.getName().replace(':', '').replace('.', '').replace('-', '')
                itemCounter = 0
                #Create Group Box
                gbServerX = QtGui.QGroupBox(self.scrollAreaWidgetContents_3)
                gbServerX.setObjectName("gbServer"+ hostStr)
                gbServerX.setTitle(str(s.getName())+ " - V"+ str(s.getVersion()))
                
                #Create Group Box Layout
                gridLayout_5 = QtGui.QGridLayout(gbServerX)
                gridLayout_5.setObjectName("gridLayout_5")
                
                #Start Time
                starttime = datetime.datetime.fromtimestamp(0) + (s.getTime() - s.getUptime())
                
                lblServerXStartedTxt = QtGui.QLabel(gbServerX)
                lblServerXStartedTxt.setObjectName("lblServer"+ hostStr +"StartedTxt")
                lblServerXStartedTxt.setText('Started:')
                gridLayout_5.addWidget(lblServerXStartedTxt, itemCounter, 0, 1, 1)
                lblServerXStarted = QtGui.QLabel(gbServerX)
                lblServerXStarted.setObjectName("lblServer"+ hostStr +"Started")
                lblServerXStarted.setText(starttime.ctime())
                gridLayout_5.addWidget(lblServerXStarted, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Uptime
                uptime = s.getUptimeUnix()
                sec =  uptime % 60
                uptime = int(uptime/60)
                min = uptime % 60
                uptime = int(uptime/60)
                hrs = uptime % 60
                uptime = int(uptime/60)
                days = uptime
                uptimeStr = ""
                if days > 1:
                    uptimeStr += str(days) +" days "
                elif days == 1:
                    uptimeStr += str(days) +" day "
                if hrs > 1:
                    uptimeStr += str(hrs) +" hrs "
                elif hrs == 1:
                    uptimeStr += str(hrs) +" hr "
                if min > 1:
                    uptimeStr += str(min) +" mins "
                elif min == 1:
                    uptimeStr += str(min) +" min "
                if sec > 1:
                    uptimeStr += str(sec) +" secs "
                elif sec == 1:
                    uptimeStr += str(sec) +" sec "
                     
                lblServerXUptimeTxt = QtGui.QLabel(gbServerX)
                lblServerXUptimeTxt.setObjectName("lblServer"+ hostStr +"UptimeTxt")
                lblServerXUptimeTxt.setText('Uptime:')
                gridLayout_5.addWidget(lblServerXUptimeTxt, itemCounter, 0, 1, 1)
                lblServerXUptime = QtGui.QLabel(gbServerX)
                lblServerXUptime.setObjectName("lblServer"+ hostStr +"Uptime")
                lblServerXUptime.setText(uptimeStr)
                gridLayout_5.addWidget(lblServerXUptime, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Total Items
                lblServerXTotalItemsTxt = QtGui.QLabel(gbServerX)
                lblServerXTotalItemsTxt.setObjectName("lblServer"+ hostStr +"TotalItemsTxt")
                lblServerXTotalItemsTxt.setText('Total Items:')
                gridLayout_5.addWidget(lblServerXTotalItemsTxt, itemCounter, 0, 1, 1)
                lblServerXTotalItems = QtGui.QLabel(gbServerX)
                lblServerXTotalItems.setObjectName("lblServer"+ hostStr +"TotalItems")
                lblServerXTotalItems.setText(str(s.getTotalItems()))
                gridLayout_5.addWidget(lblServerXTotalItems, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Current Items
                lblServerXItemsTxt = QtGui.QLabel(gbServerX)
                lblServerXItemsTxt.setObjectName("lblServer"+ hostStr +"ItemsTxt")
                lblServerXItemsTxt.setText('Current Items:')
                gridLayout_5.addWidget(lblServerXItemsTxt, itemCounter, 0, 1, 1)
                lblServerXItems = QtGui.QLabel(gbServerX)
                lblServerXItems.setObjectName("lblServer"+ hostStr +"Items")
                lblServerXItems.setText(str(s.getItems()))
                gridLayout_5.addWidget(lblServerXItems, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Total Connections
                lblServerXTotalConnectionsTxt = QtGui.QLabel(gbServerX)
                lblServerXTotalConnectionsTxt.setObjectName("lblServer"+ hostStr +"TotalConnectionsTxt")
                lblServerXTotalConnectionsTxt.setText('Total Connections:')
                gridLayout_5.addWidget(lblServerXTotalConnectionsTxt, itemCounter, 0, 1, 1)
                lblServerXTotalConnections = QtGui.QLabel(gbServerX)
                lblServerXTotalConnections.setObjectName("lblServer"+ hostStr +"TotalConnections")
                lblServerXTotalConnections.setText(str(s.getTotalConnections()))
                gridLayout_5.addWidget(lblServerXTotalConnections, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Connections
                lblServerXConnectionsTxt = QtGui.QLabel(gbServerX)
                lblServerXConnectionsTxt.setObjectName("lblServer"+ hostStr +"ConnectionsTxt")
                lblServerXConnectionsTxt.setText('Connections:')
                gridLayout_5.addWidget(lblServerXConnectionsTxt, itemCounter, 0, 1, 1)
                lblServerXConnections = QtGui.QLabel(gbServerX)
                lblServerXConnections.setObjectName("lblServer"+ hostStr +"Connections")
                lblServerXConnections.setText(str(s.getConnections()))
                gridLayout_5.addWidget(lblServerXConnections, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Hits
                lblServerXHitsTxt = QtGui.QLabel(gbServerX)
                lblServerXHitsTxt.setObjectName("lblServer"+ hostStr +"HitsTxt")
                lblServerXHitsTxt.setText('Hits:')
                gridLayout_5.addWidget(lblServerXHitsTxt, itemCounter, 0, 1, 1)
                lblServerXHits = QtGui.QLabel(gbServerX)
                lblServerXHits.setObjectName("lblServer"+ hostStr +"Hits")
                lblServerXHits.setText(str(s.getHits()))
                gridLayout_5.addWidget(lblServerXHits, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Misses
                lblServerXMissesTxt = QtGui.QLabel(gbServerX)
                lblServerXMissesTxt.setObjectName("lblServer"+ hostStr +"MissesTxt")
                lblServerXMissesTxt.setText('Misses:')
                gridLayout_5.addWidget(lblServerXMissesTxt, itemCounter, 0, 1, 1)
                lblServerXMisses = QtGui.QLabel(gbServerX)
                lblServerXMisses.setObjectName("lblServer"+ hostStr +"Misses")
                lblServerXMisses.setText(str(s.getMisses()))
                gridLayout_5.addWidget(lblServerXMisses, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Gets
                lblServerXGetsTxt = QtGui.QLabel(gbServerX)
                lblServerXGetsTxt.setObjectName("lblServer"+ hostStr +"GetsTxt")
                lblServerXGetsTxt.setText('Gets:')
                gridLayout_5.addWidget(lblServerXGetsTxt, itemCounter, 0, 1, 1)
                lblServerXGets = QtGui.QLabel(gbServerX)
                lblServerXGets.setObjectName("lblServer"+ hostStr +"Gets")
                lblServerXGets.setText(str(s.getGets()))
                gridLayout_5.addWidget(lblServerXGets, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Sets
                lblServerXSetsTxt = QtGui.QLabel(gbServerX)
                lblServerXSetsTxt.setObjectName("lblServer"+ hostStr +"SetsTxt")
                lblServerXSetsTxt.setText('Sets:')
                gridLayout_5.addWidget(lblServerXSetsTxt, itemCounter, 0, 1, 1)
                lblServerXSets = QtGui.QLabel(gbServerX)
                lblServerXSets.setObjectName("lblServer"+ hostStr +"Sets")
                lblServerXSets.setText(str(s.getSets()))
                gridLayout_5.addWidget(lblServerXSets, itemCounter, 1, 1, 1)
                itemCounter += 1
            
                #Total Space
                lblServerXTotalSpaceTxt = QtGui.QLabel(gbServerX)
                lblServerXTotalSpaceTxt.setObjectName("lblServer"+ hostStr +"TotalSpaceTxt")
                lblServerXTotalSpaceTxt.setText('Total Space:')
                gridLayout_5.addWidget(lblServerXTotalSpaceTxt, itemCounter, 0, 1, 1)
                lblServerXTotalSpace = QtGui.QLabel(gbServerX)
                lblServerXTotalSpace.setObjectName("lblServer"+ hostStr +"TotalSpace")
                lblServerXTotalSpace.setText(str(stats.getSpaceString(s.getTotalSpace())))
                gridLayout_5.addWidget(lblServerXTotalSpace, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Free Space
                lblServerXFreeSpaceTxt = QtGui.QLabel(gbServerX)
                lblServerXFreeSpaceTxt.setObjectName("lblServer"+ hostStr +"FreeSpaceTxt")
                lblServerXFreeSpaceTxt.setText('Free Space:')
                gridLayout_5.addWidget(lblServerXFreeSpaceTxt, itemCounter, 0, 1, 1)
                lblServerXFreeSpace = QtGui.QLabel(gbServerX)
                lblServerXFreeSpace.setObjectName("lblServer"+ hostStr +"FreeSpace")
                lblServerXFreeSpace.setText(str(stats.getSpaceString(s.getFreeSpace())))
                gridLayout_5.addWidget(lblServerXFreeSpace, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Used Space
                lblServerXUsedSpaceTxt = QtGui.QLabel(gbServerX)
                lblServerXUsedSpaceTxt.setObjectName("lblServer"+ hostStr +"UsedSpaceTxt")
                lblServerXUsedSpaceTxt.setText('Used Space:')
                gridLayout_5.addWidget(lblServerXUsedSpaceTxt, itemCounter, 0, 1, 1)
                lblServerXUsedSpace = QtGui.QLabel(gbServerX)
                lblServerXUsedSpace.setObjectName("lblServer"+ hostStr +"UsedSpace")
                lblServerXUsedSpace.setText(str(stats.getSpaceString(s.getUsedSpace())))
                gridLayout_5.addWidget(lblServerXUsedSpace, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Request Rate
                lblServerXRequestRateTxt = QtGui.QLabel(gbServerX)
                lblServerXRequestRateTxt.setObjectName("lblServer"+ hostStr +"RequestRateTxt")
                lblServerXRequestRateTxt.setText('Request Rate:')
                gridLayout_5.addWidget(lblServerXRequestRateTxt, itemCounter, 0, 1, 1)
                lblServerXRequestRate = QtGui.QLabel(gbServerX)
                lblServerXRequestRate.setObjectName("lblServer"+ hostStr +"RequestRate")
                lblServerXRequestRate.setText("%.2f cache requests/second"% (s.getRequestRate(),))
                gridLayout_5.addWidget(lblServerXRequestRate, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Hit Rate
                lblServerXHitRateTxt = QtGui.QLabel(gbServerX)
                lblServerXHitRateTxt.setObjectName("lblServer"+ hostStr +"HitRateTxt")
                lblServerXHitRateTxt.setText('Hit Rate:')
                gridLayout_5.addWidget(lblServerXHitRateTxt, itemCounter, 0, 1, 1)
                lblServerXHitRate = QtGui.QLabel(gbServerX)
                lblServerXHitRate.setObjectName("lblServer"+ hostStr +"HitRate")
                lblServerXHitRate.setText("%.2f cache requests/second"% (s.getHitRate(),))
                gridLayout_5.addWidget(lblServerXHitRate, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Misses Rate
                lblServerXMissRateTxt = QtGui.QLabel(gbServerX)
                lblServerXMissRateTxt.setObjectName("lblServer"+ hostStr +"MissRateTxt")
                lblServerXMissRateTxt.setText('Miss Rate:')
                gridLayout_5.addWidget(lblServerXMissRateTxt, itemCounter, 0, 1, 1)
                lblServerXMissRate = QtGui.QLabel(gbServerX)
                lblServerXMissRate.setObjectName("lblServer"+ hostStr +"MissRate")
                lblServerXMissRate.setText("%.2f cache requests/second"% (s.getMissRate(),))
                gridLayout_5.addWidget(lblServerXMissRate, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Set Rate
                lblServerXSetRateTxt = QtGui.QLabel(gbServerX)
                lblServerXSetRateTxt.setObjectName("lblServer"+ hostStr +"SetRateTxt")
                lblServerXSetRateTxt.setText('Set Rate:')
                gridLayout_5.addWidget(lblServerXSetRateTxt, itemCounter, 0, 1, 1)
                lblServerXSetRate = QtGui.QLabel(gbServerX)
                lblServerXSetRate.setObjectName("lblServer"+ hostStr +"SetRate")
                lblServerXSetRate.setText("%.2f cache requests/second"% (s.getSetRate(),))
                gridLayout_5.addWidget(lblServerXSetRate, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                #Get Rate
                lblServerXGetRateTxt = QtGui.QLabel(gbServerX)
                lblServerXGetRateTxt.setObjectName("lblServer"+ hostStr +"GetRateTxt")
                lblServerXGetRateTxt.setText('Get Rate:')
                gridLayout_5.addWidget(lblServerXGetRateTxt, itemCounter, 0, 1, 1)
                lblServerXGetRate = QtGui.QLabel(gbServerX)
                lblServerXGetRate.setObjectName("lblServer"+ hostStr +"GetRate")
                lblServerXGetRate.setText("%.2f cache requests/second"% (s.getGetRate(),))
                gridLayout_5.addWidget(lblServerXGetRate, itemCounter, 1, 1, 1)
                itemCounter += 1
                
                self.verticalLayout_6.addWidget(gbServerX)
                
            self.saServerInfo.setWidget(self.scrollAreaWidgetContents_3)
            self.horizontalLayout_6.addWidget(self.saServerInfo)
        else:
            QtGui.QMessageBox.critical(self, "Not Cluster Selected", "You do not have an Active Cluster")
                        
    def watchLiveStats(self):
        self.liveStatsDialog.show()


        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
    sys.exit(app.exec_())
    