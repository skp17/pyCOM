__author__ = "Steven Peters"
__version__ = "0.0.1"

# Standard libraries
import sys

# Third-party modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5 import QtSerialPort
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore  # TODO look into uic5 conversion

# Homemade modules
from UI.ui_mainwindow import Ui_MainWindow
from model import PortTableModel


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self._timer = QTimer(self)
        self._ports = []
        self.tableModel = PortTableModel()

        self.tableView.setModel(self.tableModel)  # Set model to table view
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self._timer.timeout.connect(self.display_ports)  # Connect timer to display function
        self._timer.start(1000)  # scan com ports every second

    def display_ports(self):
        self._ports = []
        for port in QtSerialPort.QSerialPortInfo.availablePorts():
            status = 'Unavailable' if port.isBusy() else "Available"
            self._ports.append((port.portName(), status))

        self.tableModel.ports = self._ports
        self.tableModel.layoutChanged.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
