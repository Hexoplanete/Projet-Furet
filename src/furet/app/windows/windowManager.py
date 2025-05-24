from typing import Any, Iterable, TypeVar
from PySide6 import QtWidgets, QtGui, QtCore

from furet import settings


_windows: dict[str, QtWidgets.QWidget] = {}

T = TypeVar('T', bound=QtWidgets.QWidget)


def showWindow(cls: type[T], args: Iterable[Any] = (), *, maximized=False) -> tuple[T, bool]:
    definition = f"{cls.__name__}-{hash(args)}"
    sKey = f"windows.{definition}"
    settings.setDefaultValue(sKey, QtCore.QRect())
    if definition in _windows and _windows[definition].isVisible():
        _windows[definition].activateWindow()
        return _windows[definition], False  # type: ignore

    _windows[definition] = window = cls(*args)

    oldCloseEvent = window.closeEvent

    def onWindowClose(event: QtGui.QCloseEvent, /):
        oldCloseEvent(event)
        settings.setValue(sKey, window.geometry())
    window.closeEvent = onWindowClose
    window.setGeometry(settings.value(sKey))
    if maximized:
        window.showMaximized()
    else:
        window.show()
    return window, True
