:: Convert all .ui files into python scripts
@echo OFF
echo Converting .ui files...
Scripts\pyuic5 UI\mainwindow.ui > UI\ui_mainwindow.py
echo Compiling .qrc file...
Scripts\pyrcc5 resources.qrc -o Sources\resources.py
echo Done
