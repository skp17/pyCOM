from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QAbstractTableModel


class PortTableModel(QAbstractTableModel):
    def __init__(self, ports=None):
        QAbstractTableModel.__init__(self)
        self.ports = ports or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            port = self.ports[index.row()]
            if index.column() == 0:
                return port.portName()
            else:
                status = 'Unavailable' if port.isBusy() else "Available"
                return status

        if role == Qt.ForegroundRole and index.column() == 1:
            port = self.ports[index.row()]
            if port.isBusy():
                return QColor(Qt.red)
            else:
                return QColor(Qt.darkGreen)

    def rowCount(self, index):
        return len(self.ports)

    def columnCount(self, index):
        return 2

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["Port", "Status"][section]
