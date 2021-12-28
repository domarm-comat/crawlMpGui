import sys

from PyQt6.QtWidgets import QApplication

from crawlMp.crawlMp import CrawlMp
from crawlMp.crawlers.crawler_fs import CrawlerSearchFs
from crawlMp.enums import Mode
from crawlMpGui.widgets.results_widget import ResultsWidget

app = QApplication(sys.argv)
w = ResultsWidget()
w.show()

manager = CrawlMp(CrawlerSearchFs, links=["/"], num_proc=8, pattern=".", mode=Mode.EXTENDED)
manager.start(lambda m: w.sig_update_results.emit(m.results))

app.exec()
