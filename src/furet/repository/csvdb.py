import csv
from datetime import date, datetime
import os
from types import NoneType, UnionType
from typing import Any, Callable, TypeVar, get_args, get_origin
import dataclasses


@dataclasses.dataclass
class TableDefinition:
    name: str
    id: str
    fields: dict[str, type]


_tables: dict[type, TableDefinition] = {}
_path: str
_loadedFiles: dict[str, tuple[date, list]] = {}


class TableObject:
    def __init_subclass__(cls, *, name: str | None = None, id: str = "id", fields: dict[str, type] | None = None) -> None:
        addTable(cls, TableDefinition(name or cls.__name__.lower(), id, fields))

    def __eq__(self, value: object) -> bool:
        return type(value) == type(self) and getId(self) == getId(value)

    def __ne__(self, value: object) -> bool:
        return not self == value

    def __hash__(self) -> int:
        return hash(getId(self))

    def fileSubPath(self) -> str | None:
        return None

T = TypeVar("T", bound=TableObject)

def connect(path: str):
    global _path, _loadedFiles
    _path = path
    _loadedFiles = {}


def addTable(cls: type[T], table: TableDefinition) -> None:
    _tables[cls] = table
    setSerializer(cls, lambda v: str(getId(v, cls)), lambda s, t: fetchById(cls, int(s)))


def tables() -> list[str]:
    return [t.name for t in _tables.values()]


def tableDefinition(cls: type[T] | T) -> TableDefinition:
    config = _tables[cls if type(cls) is type else type(cls)]
    if config.fields is None and dataclasses.is_dataclass(cls):
        config.fields = {f.name: f.type for f in dataclasses.fields(cls)}
    return config


def insert(objects: T | list[T]) -> None:
    objectsList: list[T] = objects if type(objects) is list else [objects] # type: ignore
    objectsPerFile: dict[str, list[T]] = {}
    for object in objectsList:
        path = getFilePath(object)
        if path not in objectsPerFile:
            objectsPerFile[path] = loadFromCsv(type(object), path)
        assignId(object)
        objectsPerFile[path].append(object)
    for path, objects in objectsPerFile.items():
        saveToCsv(objects, path)


def update(object: TableObject) -> None:
    table = type(object)
    path = getFilePath(object)
    objects = loadFromCsv(table, path)
    if object in objects:
        objects[objects.index(object)] = object
        saveToCsv(objects, path)
        return
    oldObject = fetchById(table, getId(object, table))
    oldPath = getFilePath(oldObject)
    oldObjects = loadFromCsv(table, oldPath)
    oldObjects.remove(oldObject)
    saveToCsv(oldObjects, oldPath)
    objects.append(object)
    saveToCsv(objects, path)


def fetch(table: type[T]) -> list[T]:
    filePath = getTablePath(table)
    if os.path.isfile(filePath):
        return loadFromCsv(table, filePath)
    dirPath = os.path.splitext(filePath)[0]
    if os.path.isdir(dirPath):
        objects: list[T] = []
        for root, dirs, files in os.walk(dirPath):
            for file in files:
                if file.endswith(".csv"):
                    objects += loadFromCsv(table, os.path.join(root, file))
        return objects
    return []


def fetchById(table: type[T], id: int) -> T | None:
    objects = fetch(table)
    for o in objects:
        if getId(o, table) == id:
            return o
    return None


def delete(object: TableObject) -> None:
    path = getFilePath(object)
    objects = loadFromCsv(type(object), path)
    objects.remove(object)
    saveToCsv(objects, path)


def getFilePath(object: TableObject) -> str:
    basePath = tableDefinition(object).name
    subPath = object.fileSubPath()
    return os.path.join(_path, f"{basePath}.csv" if subPath is None else os.path.join(basePath, subPath))


def getTablePath(table: type[T]) -> str:
    basePath = tableDefinition(table).name
    return os.path.join(_path, f"{basePath}.csv")


def getId(object: T, table: type[T] | None = None) -> int:
    return getattr(object, tableDefinition(table or object).id)


def assignId(object: TableObject):
    path = getTablePath(TableIds)
    ids = loadFromCsv(TableIds, path)
    config = tableDefinition(object)
    for line in ids:
        if line.table == config.name:
            newId = line.id = line.id + 1
            break
    else:
        ids.append(TableIds(config.name, newId := 1))

    saveToCsv(ids, path)
    setattr(object, config.id, newId)


_TypeAnnotation = type[Any] | str | Any
_serializers: dict[_TypeAnnotation, Callable[[Any], str]] = {}
_deserializers: dict[_TypeAnnotation, Callable[[str, _TypeAnnotation], Any]] = {}


TS = TypeVar("TS")
def setSerializer(valueType: type[TS] | _TypeAnnotation, serializer: Callable[[TS], str], deserializer: Callable[[str, type[TS] | _TypeAnnotation], TS]):
    _serializers[valueType] = serializer
    _deserializers[valueType] = deserializer

def serialize(value: Any) -> str:
    return _serializers.get(type(value), str)(value)

def deserialize(value: str, valueType: type[TS] | _TypeAnnotation) -> TS:
    return _deserializers.get(get_origin(valueType) or valueType, lambda v, t: valueType(v))(value, valueType)

LIST_SEP = '|'
DATE_FMT = "%Y-%m-%d"
setSerializer(list, lambda v: LIST_SEP.join([serialize(i) for i in v]), lambda s, t: [] if len(s) == 0 else [deserialize(i, get_args(t)[0]) for i in s.split(LIST_SEP)])
setSerializer(set, lambda v: LIST_SEP.join([serialize(i) for i in v]), lambda s, t: set() if len(s) == 0 else set(deserialize(i, get_args(t)[0]) for i in s.split(LIST_SEP)))
setSerializer(NoneType, lambda _: "", lambda s, t: None)
setSerializer(UnionType, lambda v: serialize(v), lambda s, t: None if len(s) == 0 else deserialize(s, get_args(t)[0]))
setSerializer(date, lambda v: v.strftime(DATE_FMT), lambda s, _: datetime.strptime(s, DATE_FMT).date())
setSerializer(bool, lambda v: serialize(int(v)), lambda s, _: bool(deserialize(s, int)))


CSV_SEP = ','
def saveToCsv(objects: list[T], path: str) -> None:
    try:
        if len(objects) == 0:
            os.remove(path)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=CSV_SEP)
                header = list(tableDefinition(objects[0]).fields.keys())
                writer.writerow(header)
                for o in objects:
                    try:
                        writer.writerow([serialize(getattr(o, f))
                                        for f in header])
                    except Exception as e:
                        print(f"[ERROR] Could not serialize object {o}: {e}")
                        print(f"[INFO] Skipping object {o}")
    except OSError as e:
        print(f"[ERROR] Could not write the file {path}: {e}")
        return


def loadFromCsv(table: type[T], path: str) -> list[T]:
    if not os.path.isfile(path):
        return []
    try:
        mTime = datetime.fromtimestamp(os.path.getmtime(path))
        if path in _loadedFiles and _loadedFiles[path][0] == mTime:
            return _loadedFiles[path][1]

        objects: list[T] = []
        with open(path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=CSV_SEP)
            fields = tableDefinition(table).fields
            header = next(reader)
            for row in reader:
                try:
                    objects.append(table(**{h: deserialize(c, fields[h]) for h, c in zip(header, row)}))
                except Exception as e:
                    print(f"[ERROR] Could not deserialize line {row}: {e}")
                    print(f"[INFO] Skipping line {row}")

        _loadedFiles[path] = (mTime, objects)
        return objects
    except OSError as e:
        print(f"[ERROR] Could not read the file {path}: {e}")
        return []


@dataclasses.dataclass(eq=False)
class TableIds(TableObject, name=".ids", id="table"):
    table: str
    id: int
