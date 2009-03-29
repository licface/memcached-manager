from PyQt4 import QtGui
from PyQt4 import QtCore
from Dialogs.ui_LiveStats import Ui_liveStatsDialog
import time
import threading
import Settings

class Dialog(QtGui.QDialog, Ui_liveStatsDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		self.currentCluster = None
		self.monitor = False
		self.thread = None
		self.threadInterupt = False
		
		self.settings = Settings.Settings()
		
		self.connect(self, QtCore.SIGNAL('finished(int)'), self.stopMonitor)
		
	def show(self):
		QtGui.QDialog.show(self)
		self.startMonitor()
		
	def setCluster(self, cluster):
		self.currentCluster = cluster
		
	def startMonitor(self):
		print "Start Monitor"
		self.monitor = True
		self.thread = Monitor(self)
		self.thread.start()
		
	
	def stopMonitor(self):
		print "Stop Monitor"
		self.monitor = False
		self.threadInterupt = True
		
	def toggleMonitor(self):
		if self.monitor:
			self.stopMonitor()
		else:
			self.startMonitor()
			
class Monitor(threading.Thread):
	def __init__(self, dialog):
		threading.Thread.__init__(self)
		self.dialog = dialog
		self.stats = []
		
	def run(self):
		while not self.dialog.threadInterupt:
			stats = self.dialog.currentCluster.getStats()
			self.stats.append(stats)
			if len(self.stats) > 20:
				self.stats.pop(0)
				
			print self.stats
			time.sleep(int(self.dialog.settings.settings.config['Stats']['RefreshInterval']))