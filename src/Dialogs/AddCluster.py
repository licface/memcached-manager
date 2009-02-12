from PyQt4 import QtGui
from PyQt4 import QtCore
from Dialogs.ui_AddCluster import Ui_AddClusterDialog
from Settings import Settings
from Clusters import Cluster
        
class AddCluster(QtGui.QDialog, Ui_AddClusterDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.settings = Settings()
        
        self.connect(self.btnSave, QtCore.SIGNAL('clicked()'), self.save)
        self.connect(self, QtCore.SIGNAL('finished(int)'), self.clearFields)
        
    def save(self):
        cluster = Cluster(self.txtClusterName.text())
        self.settings.servers.addCluster(cluster)
        
        self.emit(QtCore.SIGNAL('saved'), cluster)
        self.clearFields()
        
    def clearFields(self):
        self.txtClusterName.setText('')