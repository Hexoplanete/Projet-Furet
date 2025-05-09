from PySide6.QtWidgets import QApplication
import sys
from . import settings, app


def main():
    QApplication.setApplicationName("Fouille Universelle de Recueils pour Entreposage et Traitement")
    QApplication.setOrganizationDomain("github.com/Hexoplanete/Projet-Furet/")
    QApplication.setOrganizationName("Hexoplanète")

    settings.setup()
    app.setup()
    sys.exit(app.main())

if __name__ == '__main__':
    main()