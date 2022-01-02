# crawlMp-gui

![GitHub](https://img.shields.io/github/license/domarm-comat/crawlMpGui)

Graphical interface for crawlMp implemented in PyQt6.  
Results are paged into page_sized chunks.  
User can sort hits by column and apply multiple filter based on column type.

# Usage examples #

### Scripts ###

* Show help:  
  `search_fs_mp_gui --help`
* Search for .zip files  
  `search_fs_mp_gui \\.zip$`
* Get all .zip files in different directories  
  `search_fs_mp_gui \\.zip$ -l /home /usr/share`

### Python code ###

```python
import sys

from PyQt6.QtWidgets import QApplication
from crawlMp.crawlMp import CrawlMp
from crawlMp.crawlers.crawler_fs import CrawlerSearchFs
from crawlMp.enums import Mode

from crawlMpGui.widgets.results_widget import ResultsWidget

app = QApplication(sys.argv)
w = ResultsWidget()
w.show()
manager = CrawlMp(CrawlerSearchFs, links=["/"], num_proc=8, pattern="\.zip$", mode=Mode.EXTENDED)
manager.start(lambda m: w.sig_update_results.emit(m.results))
app.exec()
```

# Icons attribution

Icon made by [Roundicons](https://www.flaticon.com/authors/roundicons "Roundicons")
from [www.flaticon.com](www.flaticon.com)  
Icon made by [Smauj](https://www.flaticon.com/authors/Smauj "Smauj") from [www.flaticon.com](www.flaticon.com)  
Icon made by [deemakdaksina](https://www.flaticon.com/authors/deemakdaksina "deemakdaksina")
from [www.flaticon.com](www.flaticon.com)  