from PyQt4 import QtGui
from PyQt4 import QtCore
from ServerActions.ui_AddServer import Ui_addServerDialog
from Settings import Settings
from Servers import Server

class AddServer(QtGui.QDialog, Ui_addServerDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.connect(self.btnSave, QtCore.SIGNAL('clicked()'), self.save)
        self.connect(self, QtCore.SIGNAL('finished(int)'), self.clearFields)
        
        self.settings = Settings()
        clusters = self.settings.servers.getClusters()
        for cluster in clusters:
            self.cbCluster.insertItem(cluster.name, cluster.key)
        
    def save(self):
        ip = self.txtServerIP.text()
        port = self.txtServerPort.text()
        name = self.txtServerName.text()
        
        
        
        #pos = str(len(self.config['servers']))
        #self.config['servers'][pos] = {}
        #self.config['servers'][pos]['name'] = name
        #self.config['servers'][pos]['ip_address'] = ip
        #self.config['servers'][pos]['port'] = port
        #self.config.write()
        
        self.emit(QtCore.SIGNAL('saved'), ip, port, name)
        
    def clearFields(self):
        self.txtServerIP.setText('')
        self.txtServerPort.setText('')
        self.txtServerName.setText('')