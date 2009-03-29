from PyQt4 import QtCore
from PyQt4 import QtGui

class Slabs:
	def __init__(self, mainWindow):
		self.mainWindow = mainWindow
		
	def onFocus(self):
		"""
		Event called by MemcachedManager when this tab gains focus
		"""
		pass
	
	def onClose(self):
		pass