from typing import Any, Iterable, TypeVar
from PySide6 import QtWidgets, QtGui

from furet import settings


_windows: dict[str, QtWidgets.QWidget] = {}

T = TypeVar('T', bound=QtWidgets.QWidget)


def showWindow(cls: type[T], id: str | Any | None = None, /, *, args: Iterable[Any] = (), kwargs: dict[str, Any] = {}, maximized=False) -> tuple[T, bool]:
    definition = f"{cls.__name__}-{id}" if id else cls.__name__
    key = f"windows.{definition}"
    if definition in _windows and _windows[definition].isVisible():
        _windows[definition].activateWindow()
        return _windows[definition], False  # type: ignore

    _windows[definition] = window = cls(*args, **kwargs)
    settings.setDefaultValue(key, window.geometry())
    window.setGeometry(settings.value(key))

    oldCloseEvent = window.closeEvent
    def onWindowClose(event: QtGui.QCloseEvent, /):
        oldCloseEvent(event)
        settings.setValue(key, window.geometry())
        del _windows[definition]
    window.closeEvent = onWindowClose

    if maximized:
        window.showMaximized()
    else:
        window.show()
    return window, True
