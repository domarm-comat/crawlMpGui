from typing import Any, List

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal
from PyQt6.QtGui import QColor
from crawlMp.enums import Header_ref


class ResultsViewModel(QAbstractTableModel):
    sig_start_sorting = pyqtSignal(int, Qt.SortOrder)

    def __init__(self, hits: List[Any], header: List[Header_ref], count_offset: int = 0) -> None:
        self.hits = hits
        self.header = header
        self.count_offset = count_offset
        self.row_color_1 = QColor("#ffffff")
        self.row_color_2 = QColor("#d7efe0")
        super().__init__()

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
                unit = f" ({self.header[section][2]})" if self.header[section][2] is not None else ""
                return self.header[section][0].value + unit
            elif orientation == Qt.Orientation.Vertical:
                return f" {self.count_offset + section + 1} "

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.sig_start_sorting.emit(column, order)
