from PyQt4 import QtGui
from PyQt4 import QtCore
from LiveStats.ui_LiveStats import Ui_liveStatsDialog
import time
import threading

class Dialog(QtGui.QDialog, Ui_liveStatsDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.currentCluster = None
        self.monitor = False
        
        self.connect(self, QtCore.SIGNAL('finished(int)'), self.stopMonitor)
        
    def show(self):
        QtGui.QDialog.show(self)
        self.startMonitor()
        
    def setCluster(self, cluster):
        self.currentCluster = cluster
        
    def startMonitor(self):
        print "Start Monitor"
        self.monitor = True
    
    def stopMonitor(self):
        print "Stop Monitor"
        self.monitor = False
        
    def toggleMonitor(self):
        if self.monitor:
            self.stopMonitor()
        else:
            self.startMonitor()
            
class Monitor(threading.Thread):
    def __init__(self, Dialog):
        threading.Thread.__init__()
        
    def run(self):
        pass