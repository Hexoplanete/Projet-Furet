from argparse import Namespace
import logging
from threading import Thread
from typing import Callable
from PySide6 import QtCore, QtWidgets

from furet import updater
from furet.app.widgets.launcher.updaterWidget import UpdaterWidget
from furet.app.windows import windowManager

logger = logging.getLogger("launcher")

class LauncherWindow(QtWidgets.QMainWindow):

    def __init__(self, args: Namespace):
        super().__init__()
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)

        self._label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._label)
        self._progress = QtWidgets.QProgressBar(minimum=0, maximum=6)
        self._layout.addWidget(self._progress)
        self._stepWidget: QtWidgets.QWidget | None = None
        
        UPDATE_STEP = ("Recherche de mises à jour...", self.updateModule, UpdaterWidget)
        REPOSITORY_STEP = ("Initialisation de la base...", self.setupRepository, None)
        MIGRATION_STEP = ("Migration des données...", self.applyMigrations, None)
        PROCESSING_STEP = ("Initialisation du traitement...", self.setupProcessing, None)
        CRAWLER_STEP = ("Initialisation du crawler...", self.setupCrawler, None)
        LAUNCH_STEP = ("Lancement de l'application...", self.launchApp, None)
        QUIT_STEP = ("Fini...", lambda: None, None)

        self._steps: list[tuple[str,  Callable[[], None], type[QtWidgets.QWidget] | None]]
        if args.migrate:
            self._steps = [
                REPOSITORY_STEP,
                MIGRATION_STEP,
                QUIT_STEP
            ]
            logger.info("Configured to apply migrations")
        else:
            self._steps = [
                UPDATE_STEP,
                REPOSITORY_STEP,
                MIGRATION_STEP,
                PROCESSING_STEP,
                CRAWLER_STEP,
                LAUNCH_STEP
            ]
            logger.info("Configured to run the app")
        
        self._progress.setMaximum(len(self._steps)-1)
        self._currentStep = -1
        self._thread: Thread | None = None
        logger.info("Executing launch steps...")
        self._doStep()

    @QtCore.Slot()
    def _doStep(self):
        if self._stepWidget:
            self._layout.removeWidget(self._stepWidget)
            self._stepWidget.hide()
            self._stepWidget = None

        self._currentStep = self._currentStep+1
        name, step, widget = self._steps[self._currentStep]
        logger.info(f"{self._currentStep+1}/{len(self._steps)}: {name}")
        self._progress.setValue(self._currentStep)
        self._label.setText(name)
        if widget:
            self._stepWidget = widget()
            self._layout.addWidget(self._stepWidget)

        if self._currentStep == len(self._steps)-1:
            logger.debug(f"{self._currentStep+1}/{len(self._steps)}: Running step {name}...")
            step()
            logger.debug(f"{self._currentStep+1}/{len(self._steps)}: Step {name} finished")
            logger.info("Launch finished")
            return

        def launchStep():
            logger.debug(f"{self._currentStep+1}/{len(self._steps)}: Running step {name}...")
            step()
            logger.debug(f"{self._currentStep+1}/{len(self._steps)}: Step {name} finished")
            QtCore.QMetaObject.invokeMethod(self, "_doStep", QtCore.Qt.ConnectionType.QueuedConnection)  # type: ignore
        self._thread = Thread(target=launchStep)
        self._thread.start()

    def updateModule(self):
        currentVersion = updater.currentVersion()
        logger.info(f"Currently on {currentVersion}")
        logger.debug(f"Checking for updates...")
        latestVersion = updater.latestVersion()
        if currentVersion == latestVersion:
            logger.info("Already on latest version")
            return
        logger.info(f"A new version ({latestVersion}) is available")

        widget: UpdaterWidget = self._stepWidget # type: ignore
        doUpgrade = widget.getUpgradeChoice(latestVersion)

        if not doUpgrade:
            logger.info(f"Not upgrading")
            return
        
        logger.info(f"Upgrading to {latestVersion}...")
        updater.updateToVersion(latestVersion)
        logger.info(f"Now on {updater.currentVersion()}")

    def setupRepository(self):
        from furet import repository
        repository.setup()

    def applyMigrations(self):
        from furet import migration
        migration.applyMigrations()

    def setupProcessing(self):
        from furet import processing
        processing.setup()

    def setupCrawler(self):
        from furet import crawler
        crawler.setup()

    def launchApp(self):
        from furet.app.windows.decreeTableWindow import DecreeTableWindow
        self.close()
        windowManager.showWindow(DecreeTableWindow)