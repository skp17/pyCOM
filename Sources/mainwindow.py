__author__ = "Steven Peters"
__version__ = "1.0.1"

# Standard libraries
import sys

# Third-party modules
from PyQt5 import QtCore, QtGui, QtSerialPort, uic
from PyQt5.QtCore import QFile, QTextStream, QTimer
from PyQt5.QtWidgets import QActionGroup, QApplication, QHeaderView, QMainWindow, QMessageBox

# Homemade modules
import breeze_resources  # used for dark theme
import resources  # used to import icons
from model import PortTableModel
# from ui_mainwindow import Ui_MainWindow

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
        self._timer = QTimer(self)
        self._ports = []
        self.tableModel = PortTableModel()
        self.setWindowIcon(QtGui.QIcon(":/icons/serial_port.ico"))

        self.tableView.setModel(self.tableModel)  # Set model to table view
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.groupTheme = QActionGroup(self.menuSettings)
        self.groupTheme.addAction(self.actionLight)
        self.groupTheme.addAction(self.actionDark)
        self.groupTheme.setExclusive(True)
        self.groupTheme.triggered.connect(self.change_theme)

        self.tableView.clicked.connect(self.display_port_info)
        self.actionAbout.triggered.connect(self.show_about_dialog)

        self._timer.timeout.connect(self.display_ports)  # Connect timer to display function
        self._timer.start(1000)  # scan com ports every second

    def change_theme(self, action):
        if action == self.actionLight:
            toggle_stylesheet(":/light.qss")
        elif action == self.actionDark:
            toggle_stylesheet(":/dark/stylesheet.qss")

    def display_ports(self):
        self._ports = [port for port in QtSerialPort.QSerialPortInfo.availablePorts()]  # Run inside separate thread
        self.tableModel.ports = self._ports
        self.tableModel.layoutChanged.emit()

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


def toggle_stylesheet(path):
    """
    Toggle the stylesheet to use the desired path in the Qt resource
    system (prefixed by `:/`) or generically (a path to a file on
    system).

    :path:      A full path to a resource or file on system
    """

    # Get the QApplication instance, or crash if not set
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("No Qt Application found.")

    file = QFile(path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
