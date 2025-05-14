from typing import Any
from PySide6.QtCore import QSettings

_keyTypes: dict[str, type] = {}

def parseKey(key:str):
    return key.replace('.', '/', 1)

def setup():
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)


def setDefaultValue(key: str, defaultValue: Any, valueType: type = None):
    key = parseKey(key)
    _keyTypes[key] = valueType if valueType is not None else type(defaultValue)
    settings = QSettings()
    settings.setValue(key, settings.value(key, defaultValue=defaultValue))
    settings.sync()


def setValue(key: str, value: Any) -> object:
    key = parseKey(key)
    settings = QSettings()
    settings.setValue(key, value)
    settings.sync()

def value(key: str) -> object:
    key = parseKey(key)
    return QSettings().value(key, type=_keyTypes[key])
