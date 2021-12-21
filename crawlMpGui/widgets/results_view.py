from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal
from PyQt6.QtGui import QColor


class ResultsViewModel(QAbstractTableModel):

    sig_start_sorting = pyqtSignal(int, Qt.SortOrder)

    def __init__(self, hits: list, header: list, count_offset=0):
        self.hits = hits
        self.header = header
        self.count_offset = count_offset
        self.row_color_1 = QColor("#ffffff")
        self.row_color_2 = QColor("#d7efe0")
        QAbstractTableModel.__init__(self)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.hits)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.header)

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return f" {self.hits[index.row()][index.column()]} "
        elif role == Qt.ItemDataRole.BackgroundRole:
            return self.row_color_1 if index.row() % 2 else self.row_color_2

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.header[section]
            elif orientation == Qt.Orientation.Vertical:
                return f" {self.count_offset + section + 1} "

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.sig_start_sorting.emit(column, order)
