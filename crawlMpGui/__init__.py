from PyQt6 import QtCore
import os

__version__ = "0.0.7"

import crawlMpGui

path = os.path.dirname(crawlMpGui.__file__)
print(path)
QtCore.QDir.addSearchPath('icons', os.path.join(path, 'resources'))
