import multiprocessing
import re
import time
from multiprocessing.pool import Pool
from operator import itemgetter
from threading import Thread

from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt, QSize
from PyQt6.QtGui import QMovie, QPixmap
from PyQt6.QtWidgets import QWidget

from crawlMp.crawlMp import CrawlMp
from crawlMp.results import Results
from crawlMpGui.templates.resultsWidgetTpl import Ui_Form
from crawlMpGui.tools.filter_mp import FilterMp
from crawlMpGui.widgets.results_view import ResultsViewModel


def ss(a):
    return True if a[1].search(a[0]) else None

class ResultsWidget(QWidget, Ui_Form):
    sig_update_results = pyqtSignal(Results)
    sig_sorting_done = pyqtSignal()
    page_size = 200
    current_page = 0
    pages_count = 0
    loading = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = None
        self.setupUi(self)
        self.done_icon = QPixmap("icons:done.png").scaledToHeight(24)
        self.loading_movie = QMovie("icons:loading.gif")
        self.loading_movie.setScaledSize(QSize(24, 24))
        self.loading_movie.start()

        self.sig_update_results.connect(self.set_results)
        self.sig_sorting_done.connect(self.hits_sorted)
        self.control_widgets = (self.input_current_page, self.input_category, self.input_filler, self.button_filter)
        self.set_loading()
        self._update_enabled_states()

    def _sorting_thread(self, header_index, order):
        self.results.hits.sort(key=itemgetter(header_index), reverse=order == Qt.SortOrder.DescendingOrder)
        self.sig_sorting_done.emit()

    def _get_hits_on_page(self):
        page_start = self.current_page * self.page_size
        page_end = page_start + self.page_size
        return self.results.hits[page_start:page_end]

    def _update_enabled_states(self):
        self.button_first_page.setDisabled(self.current_page == 0 or self.loading)
        self.button_previous_page.setDisabled(self.current_page == 0 or self.loading)
        self.button_last_page.setDisabled(self.current_page == self.pages_count or self.loading)
        self.button_next_page.setDisabled(self.current_page == self.pages_count or self.loading)
        for widget in self.control_widgets:
            widget.setDisabled(self.loading)

    @pyqtSlot(Results)
    def set_results(self, results: Results) -> None:
        self.current_page = 0
        self.results = results
        self.pages_count = int(len(self.results.hits) / self.page_size)
        self.input_current_page.setMaximum(self.pages_count + 1)
        self.input_category.addItems((item[0].value for item in results.hits_header))
        self.input_current_page.setSuffix(f" / {self.pages_count + 1}")
        self.set_idle()
        self.change_current_page()

    def change_current_page(self):
        count_offset = self.current_page * self.page_size
        model = ResultsViewModel(self._get_hits_on_page(), self.results.hits_header, count_offset)
        model.sig_start_sorting.connect(self.sort_hits)
        self.input_current_page.setValue(self.current_page + 1)
        self.view_results.setModel(model)
        self._update_enabled_states()

    @pyqtSlot(int, Qt.SortOrder)
    def sort_hits(self, header_index, order):
        self.set_loading()
        sorting_thread = Thread(target=self._sorting_thread, args=(header_index, order))
        sorting_thread.start()

    @pyqtSlot()
    def hits_sorted(self):
        # self.set_idle()
        self.set_results(self.results)
        self.change_current_page()

    @pyqtSlot(int)
    def set_page(self, page):
        self.current_page = page - 1
        self.change_current_page()

    @pyqtSlot()
    def next_page(self):
        self.current_page += 1
        self.change_current_page()

    @pyqtSlot()
    def previous_page(self):
        self.current_page -= 1
        self.change_current_page()

    @pyqtSlot()
    def first_page(self):
        self.current_page = 0
        self.change_current_page()

    @pyqtSlot()
    def last_page(self):
        self.current_page = self.pages_count
        self.change_current_page()

    @pyqtSlot()
    def set_loading(self):
        self.loading = True
        self.label_status.setMovie(self.loading_movie)
        self.label_status.setToolTip("Loading")
        self._update_enabled_states()

    @pyqtSlot()
    def set_idle(self):
        self.loading = False
        self.label_status.setPixmap(self.done_icon)
        self.label_status.setToolTip("Idle")
        self._update_enabled_states()

    @pyqtSlot(int)
    def column_filter_changed(self, header_index):
        header_name, header_type, header_unit = self.results.hits_header[header_index]
        self.input_filler.clear()
        if header_type in (float, int):
            self.input_filler.setPlaceholderText("Filter by value comparison (>, <, !=, =, <=, >=)")
        else:
            self.input_filler.setPlaceholderText("Filter by regexp")

    @pyqtSlot()
    def filter_results(self):
        header_index = self.input_category.currentIndex()
        header_name, header_type, header_unit = self.results.hits_header[header_index]

        if header_type in (float, int):
            ...
        else:
            self.set_loading()
            filter_expression = re.compile(self.input_filler.text())
            Thread(target=self._regexp_filter_thread, args=(filter_expression, header_index)).start()

    def _regexp_filter_thread(self, regexp, index):
        self.results.hits = [s for s in self.results.hits if regexp.search(s[index])]
        self.sig_sorting_done.emit()
