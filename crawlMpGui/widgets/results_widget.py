import re
from copy import copy
from operator import itemgetter
from threading import Thread

from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt, QSize
from PyQt6.QtGui import QMovie, QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox
from crawlMp.results import Results

from crawlMpGui.templates.resultsWidgetTpl import Ui_Form
from crawlMpGui.widgets.results_view import ResultsViewModel


class ResultsWidget(QWidget, Ui_Form):
    sig_update_results = pyqtSignal(Results)
    sig_sorting_done = pyqtSignal()
    page_size = 200
    current_page = 0
    pages_count = 0
    loading = False

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.results = None
        self.results_copy = None
        self.setupUi(self)
        # Set icon buttons
        self.button_filter_apply.setIcon(QIcon("icons:arrow-right.png"))
        self.button_filter_reset.setIcon(QIcon("icons:reset.png"))
        # Preload resources
        self.done_icon = QPixmap("icons:done.png").scaledToHeight(24)
        self.loading_movie = QMovie("icons:loading.gif")
        self.loading_movie.setScaledSize(QSize(24, 24))
        self.loading_movie.start()

        self.sig_update_results.connect(self.set_results)
        self.sig_sorting_done.connect(self.hits_sorted)
        self.control_widgets = (
            self.input_current_page, self.input_category, self.input_filler, self.button_filter_apply,
            self.button_filter_reset)
        self.set_loading()
        self._update_enabled_states()

    def _sorting_thread(self, header_index: int, order: Qt.SortOrder) -> None:
        self.results.hits.sort(key=itemgetter(header_index), reverse=order == Qt.SortOrder.DescendingOrder)
        self.sig_sorting_done.emit()

    def _get_hits_on_page(self) -> None:
        page_start = self.current_page * self.page_size
        page_end = page_start + self.page_size
        return self.results.hits[page_start:page_end]

    def _update_enabled_states(self) -> None:
        self.button_first_page.setDisabled(self.current_page == 0 or self.loading)
        self.button_previous_page.setDisabled(self.current_page == 0 or self.loading)
        self.button_last_page.setDisabled(self.current_page == self.pages_count or self.loading)
        self.button_next_page.setDisabled(self.current_page == self.pages_count or self.loading)
        for widget in self.control_widgets:
            widget.setDisabled(self.loading)
        if self.results_copy is None:
            self.button_filter_reset.setDisabled(True)

    def _regexp_filter_thread(self, regexp: re.Pattern, index: int) -> None:
        if self.results_copy is None:
            self.results_copy = copy(self.results)
        self.results.hits = [s for s in self.results.hits if regexp.search(s[index])]
        self.sig_sorting_done.emit()

    def _eval_filter_thread(self, expression: str, index: int) -> None:
        if self.results_copy is None:
            self.results_copy = copy(self.results)
        self.results.hits = [s for s in self.results.hits if eval(f"{s[index]}{expression}")]
        self.sig_sorting_done.emit()

    @pyqtSlot(Results)
    def set_results(self, results: Results) -> None:
        self.current_page = 0
        self.results = results
        self.pages_count = int(len(self.results.hits) / self.page_size)
        self.input_current_page.setMaximum(self.pages_count + 1)
        current_selected = self.input_category.currentText()
        self.input_category.blockSignals(True)
        self.input_category.clear()
        self.input_category.addItems((item[0].value for item in results.hits_header))
        self.input_category.setCurrentText(current_selected)
        self.input_category.blockSignals(False)
        self.input_current_page.setSuffix(f" / {self.pages_count + 1}")
        self.set_idle()
        self.change_current_page()

    def change_current_page(self) -> None:
        count_offset = self.current_page * self.page_size
        model = ResultsViewModel(self._get_hits_on_page(), self.results.hits_header, count_offset)
        model.sig_start_sorting.connect(self.sort_hits)
        self.input_current_page.setValue(self.current_page + 1)
        self.view_results.setModel(model)
        self._update_enabled_states()

    @pyqtSlot(int, Qt.SortOrder)
    def sort_hits(self, header_index: int, order: Qt.SortOrder) -> None:
        self.set_loading()
        sorting_thread = Thread(target=self._sorting_thread, args=(header_index, order))
        sorting_thread.start()

    @pyqtSlot()
    def hits_sorted(self) -> None:
        self.set_results(self.results)
        self.change_current_page()

    @pyqtSlot(int)
    def set_page(self, page) -> None:
        self.current_page = page - 1
        self.change_current_page()

    @pyqtSlot()
    def next_page(self) -> None:
        self.current_page += 1
        self.change_current_page()

    @pyqtSlot()
    def previous_page(self) -> None:
        self.current_page -= 1
        self.change_current_page()

    @pyqtSlot()
    def first_page(self) -> None:
        self.current_page = 0
        self.change_current_page()

    @pyqtSlot()
    def last_page(self) -> None:
        self.current_page = self.pages_count
        self.change_current_page()

    @pyqtSlot()
    def set_loading(self) -> None:
        self.loading = True
        self.label_status.setMovie(self.loading_movie)
        self.label_status.setToolTip("Loading")
        self.setDisabled(True)
        self._update_enabled_states()

    @pyqtSlot()
    def set_idle(self) -> None:
        self.loading = False
        self.label_status.setPixmap(self.done_icon)
        self.label_status.setToolTip("Idle")
        self.setDisabled(False)
        self._update_enabled_states()

    @pyqtSlot(int)
    def column_filter_changed(self, header_index: int) -> None:
        header_name, header_type, header_unit = self.results.hits_header[header_index]
        self.input_filler.clear()
        if header_type in (float, int):
            self.input_filler.setPlaceholderText("Filter by value comparison (>, <, !=, ==, <=, >=)")
        else:
            self.input_filler.setPlaceholderText("Filter by regexp")

    @pyqtSlot()
    def filter_results(self) -> None:
        header_index = self.input_category.currentIndex()
        header_name, header_type, header_unit = self.results.hits_header[header_index]
        filter_value = self.input_filler.text()
        if self.loading:
            QMessageBox.critical(self, "Error", "Loading is in progress!")
            return
        if filter_value == "":
            QMessageBox.critical(self, "Error", "Filter input is empty!")
            return

        if header_type in (float, int):
            if not re.match("^\s?([<>!][=]?|==)\s?[+-]?([0-9]*[.])?[0-9]+$", filter_value):
                QMessageBox.critical(self, "Error", "Wrong filter pattern!")
                return
            else:
                filter_method = self._eval_filter_thread
        else:
            filter_method, filter_value = self._regexp_filter_thread, re.compile(filter_value)

        self.set_loading()
        Thread(target=filter_method, args=(filter_value, header_index)).start()

    @pyqtSlot()
    def filter_reset(self) -> None:
        if self.results_copy is not None:
            self.set_results(self.results_copy)
            self.results_copy = None
            self._update_enabled_states()
