from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_MainWindow import Ui_MainWindow
from ServerActions import Dialogs
import sys

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.connect(self.actionAddServer, QtCore.SIGNAL("triggered()"), self.displayAddServer)
        self.dialog = Dialogs.AddServer()
        self.connect(self.dialog, QtCore.SIGNAL('saved'), self.addServer)
        
        self.serverTreeItems = []
        
        
    def displayAddServer(self):
        self.dialog.show()
        
    def addServer(self, ip, port, name):
        print ip
        print port
        print name
        self.serverTreeItems.append(QListViewItem(self.serverTree, ))
        

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app, QtCore.SLOT("quit()"))
    sys.exit(app.exec_())
    