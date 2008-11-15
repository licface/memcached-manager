echo "Compiling MainWindow.ui"
pyuic4 -o ../src/ui_MainWindow.py MainWindow.ui
echo "Compiling AddServer.ui"
pyuic4 -o ../src/ServerActions/ui_AddServer.py AddServer.ui
echo "Compiling AddCluster.ui"
pyuic4 -o ../src/ServerActions/ui_AddCluster.py AddCluster.ui
echo "Compiling LiveStats.ui"
pyuic4 -o ../src/LiveStats/ui_LiveStats.py LiveStats.ui

echo "Done"
