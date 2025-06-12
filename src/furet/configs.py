from dataclasses import dataclass, field
import os
from PySide6 import QtCore

@dataclass
class AppConfig:
    scale: float = 1
    filterTreated: bool = True
    filterExpired: bool = True


@dataclass
class RepositoryConfig:
    csvRoot: str = field(default_factory=lambda: os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), 'database'))


@dataclass
class CrawlerConfig:
    ...

@dataclass
class ProcessingConfig:
    pdfDir: str = field(default_factory=lambda: os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), 'pdfs'))
    debug: bool = False

@dataclass
class WindowsConfig:
    ...
    # ["<name>-<id>"]: QtCore.QRect