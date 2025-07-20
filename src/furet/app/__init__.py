from argparse import Namespace
import logging
import os
import sys
from PySide6 import QtGui, QtWidgets
import locale

from furet import settings
from furet.settings.configs import AppConfig
from furet.app.windows import windowManager
from furet.app.windows.launcherWindow import LauncherWindow

logger = logging.getLogger("app")

def setup():
    settings.setDefaultConfig(AppConfig)

    logger.debug("Setting up locale and scale...")
    os.environ["QT_SCALE_FACTOR"] = str(settings.config(AppConfig).scale)
    locale.setlocale(locale.LC_TIME,'')

def createApplication():
    logger.debug("Creating Qt application...")
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("assets/furet-logo.ico"))
    
    logger.debug("Adding Linux Qt Plugins...")
    if os.path.isdir("/usr/lib/x86_64-linux-gnu/qt6/plugins"):
        app.addLibraryPath("/usr/lib/x86_64-linux-gnu/qt6/plugins")
        if "Breeze" in QtWidgets.QStyleFactory.keys():
            app.setStyle("Breeze")
        elif "kvantum" in QtWidgets.QStyleFactory.keys():
            app.setStyle("kvantum")
    return app


def main(args: Namespace):
    logger.info("Setting up application...")
    setup()

    logger.info("Creating Application...")
    app = createApplication()

    logger.info("Starting launcher...")
    windowManager.showWindow(LauncherWindow, args=(args,))
    code = app.exec()

    logger.info("Closed application")
    return code
