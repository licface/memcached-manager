from PyQt4 import QtCore
from PyQt4 import QtGui
import matplotlib
matplotlib.use('QT4Agg')
from matplotlib import pyplot
import datetime
import os.path
from Dialogs import LiveStats
import Settings

class Stats:
	def __init__(self, mainWindow):
		self.mainWindow = mainWindow
		self.mainWindow.connect(self.mainWindow.btnWatch, QtCore.SIGNAL("clicked()"), self.watchLiveStats)
		self.mainWindow.connect(self.mainWindow.btnRefresh, QtCore.SIGNAL('clicked()'), self._updateStats)
		
		self.liveStatsDialog = LiveStats.Dialog()
		self.settings = Settings.Settings()
		
	def onFocus(self):
		"""
		Event called when this tab gains focus
		"""
		if self.settings.settings.config['Stats']['AutoRefresh'] is True:
			self._updateStats()
			
	def onClose(self):
		self.liveStatsDialog.close()
		
	def watchLiveStats(self):
		"""
		Display the Live Stats Dialog
		"""
		if self.mainWindow.currentCluster is not None:
			self.liveStatsDialog.setCluster(self.mainWindow.currentCluster)
			self.liveStatsDialog.show()
		else:
			QtGui.QMessageBox.critical(self.mainWindow, "No Cluster Selected", "You do not have an Active Cluster")
		
	def _updateStats(self):
		"""
		Main Stats update function for the Current Active Cluster.
		
		Fires off all the seperate events needed to update each 
		stats tab and updates the prograss bar
		"""
		self.mainWindow.pbStats.setValue(0)
		if self.mainWindow.currentCluster is not None:
			matplotlib.rc('font', size=12)
			stats = self.mainWindow.currentCluster.getStats()
			self.mainWindow.pbStats.setValue(10)
			self._updateCachInfo(stats)
			self.mainWindow.pbStats.setValue(30)
			self._updateDiagrams_CacheUsage(stats)
			self.mainWindow.pbStats.setValue(60)
			self._updateDiagrams_HitsMisses(stats)
			self.mainWindow.pbStats.setValue(80)
			self._updateDiagrams_GetsSets(stats)
			self.mainWindow.pbStats.setValue(90)
			self._updateServerInfo(stats)
			self.mainWindow.pbStats.setValue(100)
		else:
			QtGui.QMessageBox.critical(self.mainWindow, "No Cluster Selected", "You do not have an Active Cluster")
		
	def _updateCachInfo(self, stats):
		"""
		Updates the Cache Info Tab
		"""
		self.mainWindow.lblItems.setText(str(stats.getTotalItems()))
		self.mainWindow.lblCurrentItems.setText(str(stats.getItems()))
		self.mainWindow.lblConnections.setText(str(stats.getTotalConnections()))
		self.mainWindow.lblCurrentConnections.setText(str(stats.getConnections()))
		self.mainWindow.lblHits.setText(str(stats.getHits()))
		self.mainWindow.lblMisses.setText(str(stats.getMisses()))
		self.mainWindow.lblGets.setText(str(stats.getGets()))
		self.mainWindow.lblSets.setText(str(stats.getSets()))
		self.mainWindow.lblThreads.setText(str(stats.getThreads()))
		
		tSpace = stats.getSpaceString(stats.getTotalSpace())
		self.mainWindow.lblSpace.setText(tSpace)
		
		fSpace = stats.getSpaceString(stats.getFreeSpace())
		self.mainWindow.lblFree.setText(fSpace)
		
		uSpace = stats.getSpaceString(stats.getUsedSpace())
		self.mainWindow.lblUsed.setText(uSpace)
		
		self.mainWindow.lblRequestRate.setText("%.2f cache requests/second"% (stats.getRequestRate(),))
		self.mainWindow.lblHitRate.setText("%.2f cache requests/second"% (stats.getHitRate(),))
		self.mainWindow.lblMissRate.setText("%.2f cache requests/second"% (stats.getMissRate(),))
		self.mainWindow.lblSetRate.setText("%.2f cache requests/second"% (stats.getSetRate(),))
		self.mainWindow.lblGetRate.setText("%.2f cache requests/second"% (stats.getGetRate(),))
		
		self.mainWindow.lblRequestRateAvg.setText("%.2f cache requests/second"% (stats.getRequestRateAvg(),))
		self.mainWindow.lblHitRateAvg.setText("%.2f cache requests/second"% (stats.getHitRateAvg(),))
		self.mainWindow.lblMissRateAvg.setText("%.2f cache requests/second"% (stats.getMissRateAvg(),))
		self.mainWindow.lblSetRateAvg.setText("%.2f cache requests/second"% (stats.getSetRateAvg(),))
		self.mainWindow.lblGetRateAvg.setText("%.2f cache requests/second"% (stats.getGetRateAvg(),))
		
	def _updateDiagrams_CacheUsage(self, stats):
		"""
		Updates the Cache Usage Diagram
		"""
		figure = pyplot.figure(figsize=(3.5,3.5), facecolor='#D4CCBA', edgecolor='#AB9675', dpi=100)
		totalSpace = stats.getTotalSpace()
		freeSpace = stats.getFreeSpace()
		values = []
		labels = []
		colors = []
		allPossibleColor = self.settings.settings.config['Graphs']['Pie']
		colorPos = 0
		count = 0
		for server in stats.getServers():
			colors.extend(allPossibleColor[colorPos])
			colorPos += 1
			if colorPos >= len(allPossibleColor):
				colorPos = 0
			count += 1
			labels.extend(("Free-"+ str(count), "Used-"+ str(count)))
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
		path = os.path.join(Settings.getSaveLocation(), 'CacheUsage.png')
		figure.savefig(path)
		self.mainWindow.lblCacheUsageGraph.setPixmap(QtGui.QPixmap(path))
		
	def _updateDiagrams_HitsMisses(self, stats):
		"""
		Updates the Hits & Misses Diagram
		"""
		figure = pyplot.figure(figsize=(3.5,3.5), facecolor='#D4CCBA', edgecolor='#AB9675')
		if (stats.getHits() + stats.getMisses()) > 0:
			hits = float(stats.getHits())/(stats.getHits() + stats.getMisses())*100
			misses = float(stats.getMisses())/(stats.getHits() + stats.getMisses())*100
		else:
			hits = 0
			misses = 0
			
		bar = pyplot.bar((0.25,1), (hits, misses), 0.5, color=self.settings.settings.config['Graphs']['HitMiss'])
		pyplot.title('Hits vs. Misses')
		pyplot.gca().set_xticklabels(('Hits', 'Misses'))
		pyplot.gca().set_xticks((0.5,1.25))
		pyplot.gca().text(bar[0].get_x()+bar[0].get_width()/2.0, 1.0*bar[0].get_height(), "%1.2f%%"%(hits,), ha='center', va='bottom')
		pyplot.gca().text(bar[1].get_x()+bar[1].get_width()/2.0, 1.0*bar[1].get_height(), "%1.2f%%"%(misses,), ha='center', va='bottom')

		path = os.path.join(Settings.getSaveLocation(), 'HitsMisses.png')
		figure.savefig(path)
		self.mainWindow.lblHitsMissesGraph.setPixmap(QtGui.QPixmap(path))
		
	def _updateDiagrams_GetsSets(self, stats):
		"""
		Updates the Gets & Sets Diagram
		"""
		figure = pyplot.figure(figsize=(3.5,3.5), facecolor='#D4CCBA', edgecolor='#AB9675')
		if (stats.getGets() + stats.getSets()) > 0:
			gets = float(stats.getGets())/(stats.getGets() + stats.getSets())*100
			sets = float(stats.getSets())/(stats.getGets() + stats.getSets())*100
		else:
			gets = 0
			sets = 0
			
		bar = pyplot.bar((0.25,1), (gets, sets), 0.5, color=self.settings.settings.config['Graphs']['GetSet'])
		pyplot.title('Gets & Sets')
		pyplot.gca().set_xticklabels(('Gets', 'Sets'))
		pyplot.gca().set_xticks((0.5,1.25))
		pyplot.gca().text(bar[0].get_x()+bar[0].get_width()/2.0, 1.0*bar[0].get_height(), "%1.2f%%"%(gets,), ha='center', va='bottom')
		pyplot.gca().text(bar[1].get_x()+bar[1].get_width()/2.0, 1.0*bar[1].get_height(), "%1.2f%%"%(sets,), ha='center', va='bottom')

		path = os.path.join(Settings.getSaveLocation(), 'GetsSets.png')
		figure.savefig(path)
		self.mainWindow.lblGetSetGraph.setPixmap(QtGui.QPixmap(path))
		
	def _updateServerInfo(self, stats):
		"""
		Updates the Server Info Tab
		"""
		#Destroy the Scroll Area
		self.mainWindow.horizontalLayout_6.removeWidget(self.mainWindow.saServerInfo)
		QtCore.Qt.WA_DeleteOnClose
		self.mainWindow.saServerInfo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.mainWindow.saServerInfo.close()
		
		#Rebuild the Scroll Area
		self.mainWindow.saServerInfo = QtGui.QScrollArea(self.mainWindow.ServerInfo)
		self.mainWindow.saServerInfo.setWidgetResizable(True)
		self.mainWindow.saServerInfo.setObjectName("saServerInfo")
		self.mainWindow.scrollAreaWidgetContents_3 = QtGui.QWidget(self.mainWindow.saServerInfo)
		self.mainWindow.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 262, 436))
		self.mainWindow.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
		self.mainWindow.verticalLayout_6 = QtGui.QVBoxLayout(self.mainWindow.scrollAreaWidgetContents_3)
		self.mainWindow.verticalLayout_6.setObjectName("verticalLayout_6")
		
		#Add each server
		for s in stats.servers:
			hostStr = s.getName().replace(':', '').replace('.', '').replace('-', '')
			itemCounter = 0
			#Create Group Box
			gbServerX = QtGui.QGroupBox(self.mainWindow.scrollAreaWidgetContents_3)
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
			
			#Threads
			lblServerXThreadsTxt = QtGui.QLabel(gbServerX)
			lblServerXThreadsTxt.setObjectName("lblServer"+ hostStr +"ThreadsTxt")
			lblServerXThreadsTxt.setText('Threads:')
			gridLayout_5.addWidget(lblServerXThreadsTxt, itemCounter, 0, 1, 1)
			lblServerXThreads = QtGui.QLabel(gbServerX)
			lblServerXThreads.setObjectName("lblServer"+ hostStr +"Connections")
			lblServerXThreads.setText(str(s.getThreads()))
			gridLayout_5.addWidget(lblServerXThreads, itemCounter, 1, 1, 1)
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
			
			self.mainWindow.verticalLayout_6.addWidget(gbServerX)
			
		self.mainWindow.saServerInfo.setWidget(self.mainWindow.scrollAreaWidgetContents_3)
		self.mainWindow.horizontalLayout_6.addWidget(self.mainWindow.saServerInfo)
