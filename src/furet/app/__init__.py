import os
import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from furet import settings
import locale

from .windows.decreeTableWindow import DecreeTableWindow

def setup():
    settings.setDefaultValue("app.scale", 1, float)
    settings.setDefaultValue("app.filter-treated", True)
    settings.setDefaultValue("app.filter-expired", True)
    locale.setlocale(locale.LC_TIME,'')

def main():
    os.environ["QT_SCALE_FACTOR"] = str(settings.value("app.scale"))
    
    app = QApplication(sys.argv)
    if os.path.isdir("/usr/lib/x86_64-linux-gnu/qt6/plugins"):
        app.addLibraryPath("/usr/lib/x86_64-linux-gnu/qt6/plugins")
        if "Breeze" in QStyleFactory.keys():
            app.setStyle("Breeze")
        elif "kvantum" in QStyleFactory.keys():
            app.setStyle("kvantum")
    window = DecreeTableWindow()
    window.showMaximized()
    return app.exec()
