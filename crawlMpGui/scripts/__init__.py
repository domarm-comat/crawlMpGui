from PyQt6 import QtCore

import crawlMpGui
import os

path = os.path.dirname(crawlMpGui.__file__)
QtCore.QDir.addSearchPath('icons', os.path.join(path, 'resources'))