:: Convert all .ui files into python scripts
@echo OFF
echo Convert .ui files...
Scripts\pyuic5 UI\mainwindow.ui > UI\ui_mainwindow.py
echo Done
