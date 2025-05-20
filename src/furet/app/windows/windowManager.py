from typing import Any, Iterable, TypeVar
from PySide6 import QtWidgets, QtGui, QtCore

from furet import settings


class WindowDefinition:
    cls: type[QtWidgets.QWidget]
    args: tuple

    def __init__(self, cls: type[QtWidgets.QWidget], args: Iterable[Any]):
        self.cls = cls
        self.args = tuple(args)

    def __eq__(self, other):
        if type(other) is not WindowDefinition:
            return False
        if self.cls != other.cls or self.args != other.args:
            return False
        return True

    def __hash__(self):
        return hash(tuple((self.cls, *self.args)))


_windows: dict[WindowDefinition, QtWidgets.QWidget] = {}

T = TypeVar('T', bound=QtWidgets.QWidget)
def showWindow(cls: type[T], args: Iterable[Any] = (), *, maximized=False) -> tuple[T, bool]:
    definition = WindowDefinition(cls, args)
    sKey = f"windows.{cls.__name__}-{hash(args)}"
    settings.setDefaultValue(sKey, QtCore.QRect())
    if definition in _windows and _windows[definition].isVisible():
        _windows[definition].activateWindow()
        return _windows[definition], False # type: ignore
    
    _windows[definition] = window = cls(*args)

    def onWindowClose(event: QtGui.QCloseEvent, /):
        settings.setValue(sKey, window.geometry())
        print(window.geometry())
    window.closeEvent = onWindowClose
    window.setGeometry(settings.value(sKey))
    print(settings.value(sKey))
    if maximized: window.showMaximized()
    else: window.show()
    return window, True
