from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget

from crawlMp.results import Results
from crawlMpGui.templates.resultsWidgetTpl import Ui_Form
from crawlMpGui.widgets.results_view import ResultsViewModel


class ResultsWidget(QWidget, Ui_Form):

    sig_update_results = pyqtSignal(Results)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.sig_update_results.connect(self.set_results)

    @pyqtSlot(Results)
    def set_results(self, results: Results) -> None:
        model = ResultsViewModel(results)
        self.view_results.setModel(model)
        self.input_category.addItems(results.hits_header)
