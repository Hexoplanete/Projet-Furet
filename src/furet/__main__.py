from PySide6.QtWidgets import QApplication
from furet import repository, app, crawler, settings


def main():
    QApplication.setApplicationName("FURET")
    QApplication.setApplicationDisplayName("Fouille Universelle de Recueils pour Entreposage et Traitement")
    QApplication.setOrganizationDomain("github.com/Hexoplanete/Projet-Furet/")
    QApplication.setOrganizationName("Hexoplanete")

    settings.setup()
    app.setup()
    crawler.setup()
    repository.setup()
    repository.readAllArretesFromFiles()
    app.main()
    pass

if __name__ == '__main__':
    main()
    