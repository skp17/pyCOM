__author__ = "Steven Peters"
__organization__ = "Personal"
__program_name__ = "pyCOM"
__copyright__ = ""
__version__ = "1.0.5"

# Standard libraries
import sys

# Third-party modules
from PyQt5 import QtCore, QtGui, QtSerialPort, uic
from PyQt5.QtWidgets import QActionGroup, QApplication, QHeaderView, QMainWindow, QMessageBox, QLabel

# Homemade modules
import breeze_resources  # used for dark theme
import resources  # used to import icons
from model import PortTableModel
from themes import apply_theme, Theme

BUNDLE = True  # used for debugging
##############################
if BUNDLE:
    from ui_mainwindow import Ui_MainWindow
else:
    qtCreatorFileValueMainWindow = r'../UI/mainwindow.ui'
    Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFileValueMainWindow)
##############################


# Decrease high DPI impact on the GUI
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


# Version
MAJOR = int(__version__.split('.')[0])
MINOR = int(__version__.split('.')[1])
REV = int(__version__.split('.')[2])


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self._ports = []  # Todo: no need for this variable
        self.tableModel = PortTableModel()
        self.setWindowTitle(__program_name__)
        self.setWindowIcon(QtGui.QIcon(":/icons/serial_port.ico"))

        # Set information that will be used by QSettings
        QtCore.QCoreApplication.setOrganizationName(__organization__)
        QtCore.QCoreApplication.setApplicationName(__program_name__)

        self.tableView.setModel(self.tableModel)  # Set model to table view
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.currentTheme = Theme.Light

        # Group the theme buttons
        self.groupTheme = QActionGroup(self.menuSettings)
        self.groupTheme.addAction(self.actionLight)
        self.groupTheme.addAction(self.actionDark)
        self.groupTheme.setExclusive(True)
        self.groupTheme.triggered.connect(self.change_theme)

        # Create overlay label to display when no COM ports are found
        self.empty_label = QLabel("No COM ports found", self.tableView)
        self.empty_label.setAlignment(QtCore.Qt.AlignCenter)
        self.empty_label.setStyleSheet("font-size: 14px; color: gray;")
        self.empty_label.setVisible(False)

        # Resize label when table resizes
        self.tableView.viewport().installEventFilter(self)

        # Connect signals
        self.tableView.clicked.connect(self.display_port_info)
        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionRefresh.triggered.connect(self.display_ports)

    def changeEvent(self, event: QtCore.QEvent):
        super().changeEvent(event)
        # The list of com ports will refresh every time the window gains focus
        if event.type() == QtCore.QEvent.ActivationChange and self.isActiveWindow():
            self.display_ports()

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent):
        # Update label position when viewport resizes
        if obj == self.tableView.viewport() and event.type() == event.Resize:
            self.adjust_empty_label()
        return super().eventFilter(obj, event)

    def showEvent(self, event: QtGui.QShowEvent):
        self.read_settings()
        super().showEvent(event)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.write_settings()
        super().closeEvent(event)

    def change_theme(self):
        if self.actionLight.isChecked():
            self.currentTheme = Theme.Light
            apply_theme(Theme.Light)
        elif self.actionDark.isChecked():
            self.currentTheme = Theme.Dark
            apply_theme(Theme.Dark)

    def adjust_empty_label(self):
        if self.tableModel.ports:
            self.empty_label.setVisible(False)
        else:
            self.empty_label.setGeometry(self.tableView.viewport().rect())  # Make label cover the viewport
            self.empty_label.setVisible(True)

    def display_ports(self):
        self._ports = [port for port in QtSerialPort.QSerialPortInfo.availablePorts()]  # Run inside separate thread
        self.tableModel.ports = self._ports
        self.tableModel.layoutChanged.emit()
        self.adjust_empty_label()

    def display_port_info(self, index):
        port = self.tableModel.ports[index.row()]
        self.txtPortInfo.setPlainText(f'Port name: {port.portName()}')
        self.txtPortInfo.appendPlainText(f'System Location: {port.systemLocation()}')
        self.txtPortInfo.appendPlainText(f'Description: {port.description()}')
        self.txtPortInfo.appendPlainText(f'Manufacturer: {port.manufacturer()}')
        self.txtPortInfo.appendPlainText(f'Product Identifier: {port.productIdentifier()}')
        self.txtPortInfo.appendPlainText(f'Vendor Identifier: {port.vendorIdentifier()}')

    def show_about_dialog(self):
        QMessageBox.about(self, 'About', f'Author: {__author__}\nVersion {__version__}')

    def read_settings(self):
        settings = QtCore.QSettings()

        size = settings.value("size", defaultValue=self.size())
        show_maximized = settings.value("showMaximized", defaultValue=self.isMaximized(), type=bool)
        theme = settings.value("theme", defaultValue=self.currentTheme.value, type=int)

        # Set window size
        if show_maximized:
            self.showMaximized()
        else:
            self.resize(size)

        # Theme
        try:
            theme = Theme(theme)
        except ValueError:
            theme = Theme.Light  # default

        if theme == Theme.Dark:
            self.actionDark.setChecked(True)
        else:
            self.actionLight.setChecked(True)

        self.change_theme()

    def write_settings(self):
        settings = QtCore.QSettings()
        settings.setValue("size", self.size())
        settings.setValue("showMaximized", self.isMaximized())
        settings.setValue("theme", self.currentTheme.value)  # save as int


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
