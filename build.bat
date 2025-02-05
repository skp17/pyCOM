:: use command "build all" to clean files, convert .ui files and create .exe
:: use command "build" to create executable
:: use command "build ui" to convert .ui files into .py files
:: use command "build clean" to delete dist/ and build/ directories
:: use command "build help" to show all commands

@ECHO OFF
IF "%1"=="" (
    SET "ALL=true"
    GOTO Clean
    ) ELSE (
        SET "ALL=false"
        IF "%1"=="exe" GOTO Executable
        IF "%1"=="ui" GOTO UI
        IF "%1"=="clean" GOTO Clean
        IF "%1"=="help" GOTO Help
    )

ECHO Error! Invalid command
GOTO Help

:Clean
ECHO Cleaning files...
If EXIST ".\build" ( rmdir ".\build" /s /q )
If EXIST ".\dist" ( rmdir ".\dist" /s /q )
IF "%ALL%"=="false" ( EXIT /b )

:UI
ECHO Compiling .qrc file...
START /B /WAIT pyrcc5 resources.qrc -o Sources\resources.py
ECHO Finished compiling Qt resource files
ECHO Converting .ui files...
cd UI\
CALL convert_ui.bat
cd ..
ECHO Finished converting .ui files
IF "%ALL%"=="false" ( EXIT /b )

:Executable
ECHO Creating executable...
CALL python.exe version.py
rem pyinstaller --onefile Sources\mainwindow.py --name pyCOM.spec
pyinstaller pyCOM.spec
EXIT /b

:Help
ECHO use command "build" to clean files, convert .ui files and create .exe
ECHO use command "build exe" to create executable
ECHO use command "build ui" to convert .ui files into .py files
ECHO use command "build clean" to delete dist/ and build/ directories
ECHO use command "build help" to show all commands
EXIT /b