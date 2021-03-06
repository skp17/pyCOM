__author__ = "Steven Peters"
__version__ = "0.0.1"

# Standard libraries
import sys

# Third-party modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5 import QtSerialPort, QtGui
from PyQt5.QtCore import QTimer

# Homemade modules
import resources
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
        self.setWindowIcon(QtGui.QIcon(":/icons/serial_port.ico"))

        self.tableView.setModel(self.tableModel)  # Set model to table view
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self._timer.timeout.connect(self.display_ports)  # Connect timer to display function
        self._timer.start(1000)  # scan com ports every second

        self.tableView.clicked.connect(self.display_port_info)

    def display_ports(self):
        self._ports = [port for port in QtSerialPort.QSerialPortInfo.availablePorts()]
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
