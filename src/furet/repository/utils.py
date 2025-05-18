
import csv
from datetime import date, datetime
import os
from typing import Any, Callable, TypeVar, get_args, get_origin
from dataclasses import fields
from types import NoneType, UnionType

_TypeAnnotation = type[Any] | str | Any
_serializers: dict[_TypeAnnotation, Callable[[Any], str]] = {}
_deserializers: dict[_TypeAnnotation, Callable[[str, _TypeAnnotation], Any]] = {}

T = TypeVar("T")


def addSerializer[T](valueType: _TypeAnnotation, serializer: Callable[[T], str], deserializer: Callable[[str, _TypeAnnotation], T]):
    _serializers[valueType] = serializer
    _deserializers[valueType] = deserializer


LIST_SEP = '|'
DATE_FMT = "%Y-%m-%d"
addSerializer(list, lambda v: LIST_SEP.join([serialize(i) for i in v]), lambda s, t: [deserialize(i, get_args(t)[0]) for i in s.split(LIST_SEP)])
addSerializer(set, lambda v: LIST_SEP.join([serialize(i) for i in v]), lambda s, t: set(deserialize(i, get_args(t)[0]) for i in s.split(LIST_SEP)))
addSerializer(NoneType, lambda _: "", lambda s, t: None)
addSerializer(UnionType, lambda v: serialize(v), lambda s, t: None if len(s) == 0 else deserialize(s, get_args(t)[0])) # optionals
addSerializer(date, lambda v: v.strftime(DATE_FMT), lambda s, _: datetime.strptime(s, DATE_FMT).date())
addSerializer(bool, lambda v: serialize(int(v)), lambda s, _: bool(deserialize(s, int)))


def serialize(value: Any) -> str:
    return _serializers.get(type(value), str)(value)


def deserialize(value: str, valueType: _TypeAnnotation) -> Any:
    return _deserializers.get(get_origin(valueType) or valueType, lambda v, t: valueType(v))(value, valueType) # type: ignore


CSV_SEP = ','
def saveToCsv(path: str, objects: list[Any], objectType: type):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=CSV_SEP)
            header = [f.name for f in fields(objectType)]
            writer.writerow(header)
            for o in objects:
                try:
                    writer.writerow([serialize(getattr(o, f)) for f in header])
                except Exception as e:
                    print(f"[ERROR] Could not serialize object {o}: {e}")
                    print(f"[INFO] Skipping object {o}")
    except OSError as e:
        print(f"[ERROR] Could not write the file {path}: {e}")
        return []


def loadFromCsv(path: str, objectType: type) -> list[Any]:
    objects: list[Any] = []
    try:
        with open(path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=CSV_SEP)
            types = {f.name: f.type for f in fields(objectType)}
            header = next(reader)
            for row in reader:
                try:
                    objects.append(objectType(**{h: deserialize(c, types[h]) for h, c in zip(header, row)}))
                except Exception as e:
                    print(f"[ERROR] Could not deserialize line {row}: {e}")
                    print(f"[INFO] Skipping line {row}")

        return objects
    except OSError as e:
        print(f"[ERROR] Could not read the file {path}: {e}")
        return []
