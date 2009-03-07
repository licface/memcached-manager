#Main Window
echo "Compiling MainWindow.ui"
pyuic4 -o ./ui_MainWindow.py MainWindow.ui

#Live Stats Dialog
echo "Compiling LiveStats.ui"
pyuic4 -o ./Dialogs/ui_LiveStats.py ./Dialogs/LiveStats.ui

#Preferences Dialog
echo "Compiling Preferences.ui"
pyuic4 -o ./Dialogs/ui_Preferences.py ./Dialogs/Preferences.ui

#Cluster/Server Add Dialog
echo "Compiling Add.ui"
pyuic4 -o ./Dialogs/ui_Add.py ./Dialogs/Add.ui

echo "Done"
