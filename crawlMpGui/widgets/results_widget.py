from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QWidget

from crawlMp.results import Results
from crawlMpGui.templates.resultsWidgetTpl import Ui_Form
from crawlMpGui.widgets.results_view import ResultsViewModel


class ResultsWidget(QWidget, Ui_Form):
    sig_update_results = pyqtSignal(Results)
    page_size = 100
    current_page = 0
    pages_count = 0

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.results = None
        self.setupUi(self)
        self.sig_update_results.connect(self.set_results)

    @pyqtSlot(Results)
    def set_results(self, results: Results) -> None:
        self.current_page = 0
        self.results = results
        self.pages_count = int(len(self.results.hits) / self.page_size)
        self.input_current_page.setMaximum(self.pages_count + 1)
        self.input_category.addItems(results.hits_header)
        self.input_current_page.setSuffix(f" / {self.pages_count + 1}")
        self.change_current_page()

    def change_current_page(self):
        count_offset = self.current_page * self.page_size
        model = ResultsViewModel(self._get_hits_on_page(), self.results.hits_header, count_offset)
        self.input_current_page.setValue(self.current_page + 1)
        self.view_results.setModel(model)
        self._update_enabled_states()

    def _get_hits_on_page(self):
        page_start = self.current_page * self.page_size
        page_end = page_start + self.page_size
        return self.results.hits[page_start:page_end]

    def _update_enabled_states(self):
        self.button_first_page.setDisabled(self.current_page == 0)
        self.button_previous_page.setDisabled(self.current_page == 0)
        self.button_last_page.setDisabled(self.current_page == self.pages_count)
        self.button_next_page.setDisabled(self.current_page == self.pages_count)

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
