import logging
from typing import Any, Iterable, TypeVar
from venv import logger
from PySide6 import QtWidgets, QtGui

from furet import settings

logger = logging.getLogger("app")

_windows: dict[str, QtWidgets.QWidget] = {}

T = TypeVar('T', bound=QtWidgets.QWidget)


def showWindow(cls: type[T], id: str | Any | None = None, /, *, args: Iterable[Any] = (), kwargs: dict[str, Any] = {}, maximized=False) -> tuple[T, bool]:
    definition = f"{cls.__name__}-{id}" if id else cls.__name__
    key = f"windows.{definition}"

    logger.debug(f'Request to show window {definition}')
    if definition in _windows and _windows[definition].isVisible():
        _windows[definition].activateWindow()
        logger.info(f'Activated window {definition}')
        return _windows[definition], False  # type: ignore

    logger.debug(f'Creating window {definition}...')
    _windows[definition] = window = cls(*args, **kwargs)

    logger.debug(f'Restoring window {definition} geometry...')
    settings.setDefaultValue(key, window.geometry())
    window.setGeometry(settings.value(key))
    logger.debug(f'Restored window {definition} geometry {settings.value(key)}')

    oldCloseEvent = window.closeEvent
    def onWindowClose(event: QtGui.QCloseEvent, /):
        oldCloseEvent(event)
        logger.debug(f'Saving window {definition} geometry {settings.value(key)}...')
        settings.setValue(key, window.geometry())
        logger.debug(f'Saved window {definition} geometry {window.geometry()}')
        del _windows[definition]
        logger.info(f'Window {definition} closed')
    window.closeEvent = onWindowClose

    if maximized:
        window.showMaximized()
    else:
        window.show()
    logger.info(f'Created window {definition}')
    return window, True
