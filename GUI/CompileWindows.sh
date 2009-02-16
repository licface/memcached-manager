echo "Compiling MainWindow.ui"
pyuic4 -o ../src/ui_MainWindow.py MainWindow.ui
echo "Compiling LiveStats.ui"
pyuic4 -o ../src/Dialogs/ui_LiveStats.py LiveStats.ui
echo "Compiling Preferences.ui"
pyuic4 -o ../src/Dialogs/ui_Preferences.py Preferences.ui
echo "Compiling Add.ui"
pyuic4 -o ../src/Dialogs/ui_Add.py Add.ui

echo "Done"
