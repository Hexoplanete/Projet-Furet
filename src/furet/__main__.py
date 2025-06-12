from PySide6.QtWidgets import QApplication
import os
from furet import migration, repository, app, crawler, settings
from PySide6 import QtCore
import argparse

def setup():
    QApplication.setApplicationName("FURET")
    QApplication.setApplicationDisplayName("Fouille Universelle de Recueils pour Entreposage et Traitement")
    QApplication.setOrganizationDomain("github.com/Hexoplanete/Projet-Furet/")
    QApplication.setOrganizationName("Hexoplanete")
    os.makedirs(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), exist_ok=True)

def main():
    parser = argparse.ArgumentParser(
        prog="furet",
        description="Fouille Universelle de Recueils pour Entreposage et Traitement",
    )
    parser.add_argument("-m", "--migrate", default=False, action="store_true", help="Execute les migrations sans lancer l'interface")

    args = parser.parse_args()

    setup()
    settings.setup()
    repository.setup()
    migration.migrate()
    if args.migrate:
        return
    crawler.setup()
    app.setup()

    app.main()

if __name__ == '__main__':
    main()
    