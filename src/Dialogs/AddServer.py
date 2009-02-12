from PyQt4 import QtGui
from PyQt4 import QtCore
from Dialogs.ui_AddServer import Ui_addServerDialog
from Settings import Settings

class AddServer(QtGui.QDialog, Ui_addServerDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.connect(self.btnSave, QtCore.SIGNAL('clicked()'), self.save)
        self.connect(self, QtCore.SIGNAL('finished(int)'), self.clearFields)
        
        self.settings = Settings()
        self.updateClusters()
                
    def save(self):
        cluster = self.settings.servers.getCluster(self.cbCluster.currentText())
        ip = self.txtServerIP.text()
        port = self.txtServerPort.text()
        name = self.txtServerName.text()
        
        server = self.settings.servers.addServer(cluster, name, ip, port)
        
        self.emit(QtCore.SIGNAL('saved'), cluster, server)
        self.clearFields()
        
    def clearFields(self):
        self.txtServerIP.setText('')
        self.txtServerPort.setText('')
        self.txtServerName.setText('')
        
    def updateClusters(self):
        self.cbCluster.clear()
        clusters = self.settings.servers.getClusters()
        for cluster in clusters:
            self.cbCluster.addItem(cluster.name)
            
    def addCluster(self, cluster):
        self.cbCluster.addItem(cluster.name)