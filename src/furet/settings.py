from dataclasses import fields
import logging
import re
from typing import Any, TypeVar
from PySide6.QtCore import QSettings

logger = logging.getLogger("settings")

def parseKey(key: str):
    return key.replace('.', '/', 1)


_keyTypes: dict[str, type[Any] | str | Any] = {}


def setDefaultValue(key: str, defaultValue: Any, valueType: type | None = None):
    key = parseKey(key)
    logger.debug(f"Setting default value of {key} to {defaultValue}...")
    _keyTypes[key] = valueType if valueType is not None else type(defaultValue)
    settings = QSettings()
    settings.setValue(key, settings.value(key, defaultValue=defaultValue))
    settings.sync()
    logger.debug(f"Set default value of {key} to {defaultValue}")


def setValue(key: str, value: Any) -> Any:
    key = parseKey(key)
    logger.debug(f"Setting value of {key} to {value}...")
    settings = QSettings()
    settings.setValue(key, value)
    settings.sync()
    logger.info(f"Set value of {key} to {value}")


def value(key: str) -> Any:
    key = parseKey(key)
    return QSettings().value(key, type=_keyTypes[key])


def parseConfigKey(config: str, field: str) -> str:
    return re.sub(r'([a-z])([A-Z])', r'\1-\2', f"{config.removesuffix("Config")}/{field}").lower()


T = TypeVar("T")


def setDefaultConfig(config: type[T]):
    name = config.__name__
    logger.debug(f"Adding default config {name}...")
    settings = QSettings()
    defaults = config()
    for f in fields(config):
        key = parseConfigKey(name, f.name)
        settings.setValue(key, settings.value(key, defaultValue=getattr(defaults, f.name)))
        _keyTypes[key] = f.type # for direct access
    settings.sync()
    logger.debug(f"Added default config {defaults}")


def setConfig(config: object):
    name = type(config).__name__
    logger.debug(f"Setting config {config}...")
    settings = QSettings()
    [settings.setValue(parseConfigKey(name, f.name), getattr(config, f.name)) for f in fields(config)]
    settings.sync()
    logger.info(f"Set config {config}")


def config(config: type[T]) -> T:
    settings = QSettings()
    name = config.__name__
    return config(**{f.name: settings.value(parseConfigKey(name, f.name), type=f.type) for f in fields(config)})