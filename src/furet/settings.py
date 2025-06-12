from dataclasses import fields
import re
from typing import Any, TypeVar
from PySide6.QtCore import QSettings


def setup():
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)


def parseKey(key: str):
    return key.replace('.', '/', 1)


_keyTypes: dict[str, type] = {}


def setDefaultValue(key: str, defaultValue: Any, valueType: type = None):
    key = parseKey(key)
    _keyTypes[key] = valueType if valueType is not None else type(defaultValue)
    settings = QSettings()
    settings.setValue(key, settings.value(key, defaultValue=defaultValue))
    settings.sync()


def setValue(key: str, value: Any) -> Any:
    key = parseKey(key)
    settings = QSettings()
    settings.setValue(key, value)
    settings.sync()


def value(key: str) -> Any:
    key = parseKey(key)
    return QSettings().value(key, type=_keyTypes[key])


def parseConfigKey(config: str, field: str) -> str:
    return re.sub(r'([a-z])([A-Z])', r'\1-\2', f"{config.removesuffix("Config")}/{field}").lower()


T = TypeVar("T")


def setDefaultConfig(config: type[T]):
    settings = QSettings()
    name = config.__name__
    defaults = config()
    for f in fields(config):
        key = parseConfigKey(name, f.name)
        settings.setValue(key, settings.value(key, defaultValue=getattr(defaults, f.name)))
        _keyTypes[key] = f.type # for direct access
    settings.sync()


def setConfig(config: object):
    settings = QSettings()
    name = type(config).__name__
    [settings.setValue(parseConfigKey(name, f.name), getattr(config, f.name)) for f in fields(config)]
    settings.sync()


def config(config: type[T]) -> T:
    settings = QSettings()
    name = config.__name__
    return config(**{f.name: settings.value(parseConfigKey(name, f.name), type=f.type) for f in fields(config)})