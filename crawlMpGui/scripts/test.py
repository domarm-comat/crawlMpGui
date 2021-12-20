import sys

from PyQt6.QtWidgets import QApplication, QWidget

from crawlMpGui.widgets.results_widget import ResultsWidget

from crawlMp.crawlMp import CrawlMp
from crawlMp.crawlers.crawler_fs import CrawlerSearchFs
from crawlMp.snippets.output import print_summary

app = QApplication(sys.argv)
w = ResultsWidget()
w.show()

manager = CrawlMp(CrawlerSearchFs, links=["/home"], num_proc=8, pattern="\.zip$")
manager.start(lambda m: w.sig_update_results.emit(m.results))

app.exec()
