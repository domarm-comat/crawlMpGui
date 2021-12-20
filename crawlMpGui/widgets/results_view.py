from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor

from crawlMp.results import Results


class ResultsViewModel(QAbstractTableModel):

    def __init__(self, results: Results):
        self.results = results
        self.row_color_1 = QColor("#eeeeee")
        self.row_color_2 = QColor("#d7d7d7")
        QAbstractTableModel.__init__(self)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.results.hits)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.results.hits_header)

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.results.hits[index.row()][index.column()]
        elif role == Qt.ItemDataRole.BackgroundRole:
            return self.row_color_1 if index.row() % 2 else self.row_color_2

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.results.hits_header[section]
            elif orientation == Qt.Orientation.Vertical:
                return section + 1