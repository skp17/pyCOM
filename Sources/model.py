from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QAbstractTableModel


class PortTableModel(QAbstractTableModel):
    def __init__(self, ports=None):
        QAbstractTableModel.__init__(self)
        self.ports = ports or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.ports[index.row()][index.column()]
            return data

        if role == Qt.TextColorRole and index.column() == 1:
            status = self.ports[index.row()][index.column()]
            if status == 'Available':
                return QColor(Qt.darkGreen)
            else:
                return QColor(Qt.red)

    def rowCount(self, index):
        return len(self.ports)

    def columnCount(self, index):
        return 2

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["Port", "Status"][section]
