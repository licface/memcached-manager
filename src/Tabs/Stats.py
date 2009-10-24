from PyQt4 import QtCore
from PyQt4 import QtGui
import matplotlib
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
		
		self.mainWindow.lblSpace.setText(stats.getFormatedTotalSpace())
		self.mainWindow.lblFree.setText(stats.getFormatedFreeSpace())
		self.mainWindow.lblUsed.setText(stats.getFormatedUsedSpace())
		
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
				
			if(server.Bytes > 0):
				usedPerc = (float(server.Bytes)/totalSpace)*100
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
		
		def renderItem(gbBox, grid, serverName, itemCounter, itemName, itemValue):
			cleanName = itemName.replace(':', '').replace(' ', '')
			lblServerXStartedTxt = QtGui.QLabel(gbBox)
			lblServerXStartedTxt.setObjectName("lblServer"+ serverName+cleanName +"Txt")
			lblServerXStartedTxt.setText(itemName+':')
			grid.addWidget(lblServerXStartedTxt, itemCounter, 0, 1, 1)
			lblServerXStarted = QtGui.QLabel(gbBox)
			lblServerXStarted.setObjectName("lblServer"+ serverName+cleanName)
			lblServerXStarted.setText(str(itemValue))
			grid.addWidget(lblServerXStarted, itemCounter, 1, 1, 1)
		
		#Add each server
		for s in stats.servers:
			hostStr = str(s.Name).replace(':', '').replace('.', '').replace('-', '')
			itemCounter = 0
			#Create Group Box
			gbServerX = QtGui.QGroupBox(self.mainWindow.scrollAreaWidgetContents_3)
			gbServerX.setObjectName("gbServer"+ hostStr)
			gbServerX.setTitle(str(s.Name)+ " - V"+ str(s.Version))
			
			#Create Group Box Layout
			gridLayout_5 = QtGui.QGridLayout(gbServerX)
			gridLayout_5.setObjectName("gridLayout_5")
			
			#PID
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'PID', s.PID)
			itemCounter += 1
			
			#Start Time
			starttime = (datetime.datetime.fromtimestamp(0) + (s.Time - s.Uptime)).ctime()
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Started', starttime)
			itemCounter += 1
			
			#Uptime
			uptime = s.UptimeTimestamp
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
				 
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Uptime', uptimeStr)
			itemCounter += 1
			
			#Total Items
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Total Items', s.TotalItems)
			itemCounter += 1
			
			#Current Items
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Current Items', s.CurrItems)
			itemCounter += 1
			
			#Total Connections
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Total Connections', s.TotalItems)
			itemCounter += 1
			
			#Connections
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Connections', s.CurrConnections)
			itemCounter += 1
		
			#Total Space
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Total Space', s.getFormatedTotalSpace())
			itemCounter += 1
			
			#Free Space
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Free Space', s.getFormatedFreeSpace())
			itemCounter += 1
			
			#Used Space
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Used Space', s.getFormatedUsedSpace())
			itemCounter += 1
			
			#Requests
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Total Requests', s.getTotalRequests())
			itemCounter += 1
			
			#Gets
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Gets', s.CMDGet)
			itemCounter += 1
			
			#Sets
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Sets', s.CMDSet)
			itemCounter += 1
			
			#Flushes
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Flushes', s.CMDFlush)
			itemCounter += 1
			
			#Evictions
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Evictions', s.Evictions)
			itemCounter += 1
			
			#Get Hits
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Get Hits', s.GetHits)
			itemCounter += 1
			
			#Get Misses
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Get Misses', s.GetMisses)
			itemCounter += 1
			
			#Delete Hits
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Delete Hits', s.DeleteHits)
			itemCounter += 1
			
			#Delete Misses
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Delete Misses', s.DeleteMisses)
			itemCounter += 1
			
			#Incr Hits
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Incr Hits', s.IncrHits)
			itemCounter += 1
			
			#Incr Misses
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Incr Misses', s.IncrMisses)
			itemCounter += 1
			
			#Decr Hits
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Decr Hits', s.DecrHits)
			itemCounter += 1
			
			#Decr Misses
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Decr Misses', s.DecrMisses)
			itemCounter += 1
			
			#Cas Hits
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'CAS Hits', s.CasHits)
			itemCounter += 1
			
			#Cas Misses
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'CAS Misses', s.CasMisses)
			itemCounter += 1
			
			#Cas Badval
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'CAS Misses', s.CasBadval)
			itemCounter += 1
			
			#Bytes Written
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Net Out', s.getFormatedBytesWrite())
			itemCounter += 1
			
			#Bytes Read
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Net In', s.getFormatedBytesRead())
			itemCounter += 1
			
			#Pointer Size
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Pointer Size', s.PointerSize)
			itemCounter += 1
			
			#Threads
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Threads', s.Threads)
			itemCounter += 1
			
			#RUsage User
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'CPU User Time', s.RUsageUser)
			itemCounter += 1
			
			#RUsage System
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'CPU System Time', s.RUsageSystem)
			itemCounter += 1
			
			#Connection Structures
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Connection Structures', s.ConnectionStructures)
			itemCounter += 1
			
			#Accepting Conns
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Accepting Connections', s.AcceptingConns)
			itemCounter += 1
			
			#Listen Disabled Num
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Listen Disabled Num', s.ListenDisabledNum)
			itemCounter += 1
			
			#Conn Yields
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Connection Yields', s.ConnYields)
			itemCounter += 1
			
			#Request Rate
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Request Rate', "%.2f cache requests/second"% (s.getRequestRate(),))
			itemCounter += 1
			
			#Hit Rate
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Hit Rate', "%.2f cache requests/second"% (s.getHitRate(),))
			itemCounter += 1
			
			#Misses Rate
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Miss Rate', "%.2f cache requests/second"% (s.getMissRate(),))
			itemCounter += 1
			
			#Set Rate
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Set Rate', "%.2f cache requests/second"% (s.getSetRate(),))
			itemCounter += 1
			
			#Get Rate
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Get Rate', "%.2f cache requests/second"% (s.getGetRate(),))
			itemCounter += 1
			
			#Eviction Rate
			renderItem(gbServerX, gridLayout_5, hostStr, itemCounter, 'Eviction Rate', "%.2f cache requests/second"% (s.getEvictionRate(),))
			itemCounter += 1
			
			self.mainWindow.verticalLayout_6.addWidget(gbServerX)
			
		self.mainWindow.saServerInfo.setWidget(self.mainWindow.scrollAreaWidgetContents_3)
		self.mainWindow.horizontalLayout_6.addWidget(self.mainWindow.saServerInfo)
