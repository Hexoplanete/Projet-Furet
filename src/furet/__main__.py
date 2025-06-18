import logging
import argparse
import os
from PySide6 import QtCore, QtWidgets
from furet import app

logger = logging.getLogger("module")
def setup(args: argparse.Namespace):
    logger.debug("Setting up Qt...")
    QtWidgets.QApplication.setApplicationName("FURET")
    QtWidgets.QApplication.setApplicationDisplayName("Fouille Universelle de Recueils pour Entreposage et Traitement")
    QtWidgets.QApplication.setOrganizationDomain("github.com/Hexoplanete/Projet-Furet/")
    QtWidgets.QApplication.setOrganizationName("Hexoplanete")
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.Format.IniFormat)

    logger.debug("Making sure AppDataLocation exists...")
    os.makedirs(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), exist_ok=True)


def main():
    parser = argparse.ArgumentParser(
        prog="furet",
        description="Fouille Universelle de Recueils pour Entreposage et Traitement",
    )
    parser.add_argument("-m", "--migrate", default=False, action="store_true", help="Execute les migrations sans lancer l'application")
    parser.add_argument("--log", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level")

    args = parser.parse_args()

    logging.basicConfig(format="[%(asctime)s] [%(threadName)s/%(levelname)s] [%(name)s] %(message)s", level=args.log.upper())
    logger.info(f"Log level set to {args.log.upper()}")


    logger.info("Setting up module...")
    setup(args)
    logger.info("Launching application...")
    app.main(args)
    logger.info("Exit")

if __name__ == '__main__':
    main()
