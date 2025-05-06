import os
import sys
from PySide6.QtWidgets import QApplication, QStyleFactory

from .windows.DecreeTableWindow import DecreeTableWindow

def run_app():
    app = QApplication(sys.argv)
    if os.path.isdir("/usr/lib/x86_64-linux-gnu/qt6/plugins/"):
        app.addLibraryPath("/usr/lib/x86_64-linux-gnu/qt6/plugins/")
        if "Breeze" in QStyleFactory.keys():
            app.setStyle("Breeze")
        elif "kvantum" in QStyleFactory.keys():
            app.setStyle("kvantum")

    window = DecreeTableWindow()
    window.showMaximized()
    return app.exec()
