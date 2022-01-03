from PyQt6 import QtCore
import os

__version__ = "0.0.8"

import crawlMpGui


def set_resources():
    QtCore.QDir.addSearchPath('icons', os.path.join(os.path.dirname(crawlMpGui.__file__), 'resources'))

set_resources()