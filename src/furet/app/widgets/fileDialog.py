import os
from typing import Any, Sequence, List, Tuple, TypeVar
from PySide6 import QtCore, QtWidgets

from furet import settings

T = TypeVar("T", bound=str|QtCore.QUrl)

class FileDialog(QtWidgets.QFileDialog):

    @staticmethod
    def getExistingDirectory(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: str = "", options: QtWidgets.QFileDialog.Option | None = None) -> str: # type: ignore
        if options is not None: path = QtWidgets.QFileDialog.getExistingDirectory(parent, caption, FileDialog.getLastPath(id, dir), options)
        else: path = QtWidgets.QFileDialog.getExistingDirectory(parent, caption, FileDialog.getLastPath(id, dir))
        if path: FileDialog.setLastPath(id, path)
        return path

    @staticmethod
    def getExistingDirectoryUrl(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: QtCore.QUrl | str = "", options: QtWidgets.QFileDialog.Option | None = None, supportedSchemes: Sequence[str] = ()) -> QtCore.QUrl: # type: ignore
        if options is not None: path = QtWidgets.QFileDialog.getExistingDirectoryUrl(parent, caption, FileDialog.getLastPath(id, dir), options, supportedSchemes)
        else: path = QtWidgets.QFileDialog.getExistingDirectoryUrl(parent, caption, FileDialog.getLastPath(id, dir), supportedSchemes=supportedSchemes)
        if path: FileDialog.setLastPath(id, path.toString())
        return path

    @staticmethod
    def getOpenFileName(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: str = "", filter: str = "", selectedFilter: str = "", options: QtWidgets.QFileDialog.Option | None = None) -> Tuple[str, str]: # type: ignore
        if options is not None: path = QtWidgets.QFileDialog.getOpenFileName(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, options)
        else: path = QtWidgets.QFileDialog.getOpenFileName(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter)
        if path[0]: FileDialog.setLastPath(id, os.path.dirname(path[0]))
        return path


    @staticmethod
    def getOpenFileNames(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: str = "", filter: str = "", selectedFilter: str = "", options: QtWidgets.QFileDialog.Option | None = None) -> Tuple[List[str], str]: # type: ignore
        if options is not None: paths = QtWidgets.QFileDialog.getOpenFileNames(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, options)
        else: paths = QtWidgets.QFileDialog.getOpenFileNames(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter)
        if paths[0]: FileDialog.setLastPath(id, os.path.dirname(paths[0][0]))
        return paths


    @staticmethod
    def getOpenFileUrl(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: QtCore.QUrl | str = "", filter: str = "", selectedFilter: str = "", options: QtWidgets.QFileDialog.Option | None = None, supportedSchemes: Sequence[str] = ()) -> Tuple[QtCore.QUrl, str]: # type: ignore
        if options is not None: path = QtWidgets.QFileDialog.getOpenFileUrl(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, options, supportedSchemes)
        else: path = QtWidgets.QFileDialog.getOpenFileUrl(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, supportedSchemes=supportedSchemes)
        if path[0]: FileDialog.setLastPath(id, os.path.dirname(path[0].toString()))
        return path


    @staticmethod
    def getOpenFileUrls(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: QtCore.QUrl | str = "", filter: str = "", selectedFilter: str = "", options: QtWidgets.QFileDialog.Option | None = None, supportedSchemes: Sequence[str] = ()) -> Tuple[List[QtCore.QUrl], str]: # type: ignore
        if options is not None: paths = QtWidgets.QFileDialog.getOpenFileUrls(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, options, supportedSchemes)
        else: paths = QtWidgets.QFileDialog.getOpenFileUrls(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, supportedSchemes=supportedSchemes)
        if paths[0]: FileDialog.setLastPath(id, os.path.dirname(paths[0][0].toString()))
        return paths


    @staticmethod
    def getSaveFileName(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: str = "", filter: str = "", selectedFilter: str = "", options: QtWidgets.QFileDialog.Option | None = None) -> Tuple[str, str]: # type: ignore
        if options is not None: path = QtWidgets.QFileDialog.getSaveFileName(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, options)
        else: path = QtWidgets.QFileDialog.getSaveFileName(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter)
        if path[0]: FileDialog.setLastPath(id, os.path.dirname(path[0]))
        return path


    @staticmethod
    def getSaveFileUrl(parent: QtWidgets.QWidget | None = None, caption: str = "", id: str | Any | None = None, dir: QtCore.QUrl | str = "", filter: str = "", selectedFilter: str = "", options: QtWidgets.QFileDialog.Option | None = None, supportedSchemes: Sequence[str] = ()) -> Tuple[QtCore.QUrl, str]: # type: ignore
        if options is not None: path = QtWidgets.QFileDialog.getSaveFileUrl(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, options, supportedSchemes)
        else: path = QtWidgets.QFileDialog.getSaveFileUrl(parent, caption, FileDialog.getLastPath(id, dir), filter, selectedFilter, supportedSchemes=supportedSchemes)
        if path[0]: FileDialog.setLastPath(id, os.path.dirname(path[0].toString()))
        return path


    @staticmethod
    def getLastPath(id: str | Any | None, dir: T) -> T:
        if id is None: return dir
        key = f"file-dialogs.{id}"
        settings.setDefaultValue(key, dir)
        return settings.value(key)
        
    @staticmethod
    def setLastPath(id: str | Any | None, dir: T):
        if id is None: return
        key = f"file-dialogs.{id}"
        settings.setValue(key, dir)
        