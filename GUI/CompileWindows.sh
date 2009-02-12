echo "Compiling MainWindow.ui"
pyuic4 -o ../src/ui_MainWindow.py MainWindow.ui
echo "Compiling AddServer.ui"
pyuic4 -o ../src/Dialogs/ui_AddServer.py AddServer.ui
echo "Compiling AddCluster.ui"
pyuic4 -o ../src/Dialogs/ui_AddCluster.py AddCluster.ui
echo "Compiling LiveStats.ui"
pyuic4 -o ../src/Dialogs/ui_LiveStats.py LiveStats.ui
echo "Compiling Preferences.ui"
pyuic4 -o ../src/Dialogs/ui_Preferences.py Preferences.ui

echo "Done"
