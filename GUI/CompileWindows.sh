echo "Compiling MainWindow.ui"
pyuic4 -o ../src/ui_MainWindow.py MainWindow.ui
echo "Compiling AddServer.ui"
pyuic4 -o ../src/ServerActions/ui_AddServer.py AddServer.ui

echo "Done"
