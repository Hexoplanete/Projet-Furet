import csv
from datetime import date, datetime
import logging
import os
from types import NoneType, UnionType
from typing import Any, Callable, TypeVar, get_args, get_origin
import dataclasses

logger = logging.getLogger("csvdb")

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
    logger.info(f"DB initialised on path \"{path}\"")


def addTable(cls: type[T], table: TableDefinition) -> None:
    _tables[cls] = table
    setSerializer(cls, lambda v: str(getId(v, cls)), lambda s, t: fetchById(cls, int(s)))
    logger.info(f"Added table {table}")


def tables() -> list[str]:
    return [t.name for t in _tables.values()]


def tableDefinition(cls: type[T] | T) -> TableDefinition:
    config = _tables[cls if type(cls) is type else type(cls)]
    if config.fields is None and dataclasses.is_dataclass(cls):
        config.fields = {f.name: f.type for f in dataclasses.fields(cls)}
    return config


def insert(objects: T | list[T]) -> None:
    logger.debug(f"Inserting {objects}...")
    objectsList: list[T] = objects if type(objects) is list else [objects] # type: ignore
    objectsPerFile: dict[str, list[T]] = {}
    for i, object in enumerate(objectsList):
        logger.debug(f"{i+1}/{len(objectsList)}: Inserting {object}...")
        path = getFilePath(object)
        if path not in objectsPerFile:
            objectsPerFile[path] = loadFromCsv(type(object), path)
        assignId(object)
        objectsPerFile[path].append(object)
        logger.debug(f"{i+1}/{len(objectsList)}: Inserted {object} into \"{path}\"")

    logger.debug(f"Saving files {objectsPerFile.keys()}...")
    for path, objects in objectsPerFile.items():
        saveToCsv(objects, path)
    logger.info(f"Inserted {objects}")


def update(objects: T | list[T]) -> None:
    logger.debug(f"Updating {objects}...")
    objectsList: list[T] = objects if type(objects) is list else [objects] # type: ignore
    objectsPerFile: dict[str, list[T]] = {}

    for i, object in enumerate(objectsList):
        logger.debug(f"{i+1}/{len(objectsList)}: Updating {object}...")
        table = type(object)
        oldObject = fetchById(table, getId(object, table))
        if oldObject is None:
            logger.debug(f"{i+1}/{len(objectsList)}: Skipping {object} as it is not in the DB")
            continue
        
        newPath = getFilePath(object)
        if newPath not in objectsPerFile:
            objectsPerFile[newPath] = loadFromCsv(type(object), newPath)
        
        oldPath = getFilePath(oldObject)
        if oldPath == newPath:
            # objects is in the same file, simple replace the instance
            objectsPerFile[newPath][objectsPerFile[newPath].index(object)] = object
            logger.debug(f"{i+1}/{len(objectsList)}: Updated {object} from \"{newPath}\"")
        else:
            # otherwise, remove the old one and add the new one to the new file
            if oldPath not in objectsPerFile:
                objectsPerFile[oldPath] = loadFromCsv(type(object), oldPath)
            objectsPerFile[oldPath].remove(oldObject)
            objectsPerFile[newPath].append(object)
            logger.debug(f"{i+1}/{len(objectsList)}: Updated {object} from \"{oldPath}\" to \"{newPath}\"")

    logger.debug(f"Saving files {objectsPerFile.keys()}...")
    for newPath, objects in objectsPerFile.items():
        saveToCsv(objects, newPath)
    logger.info(f"Updated {objects}")


def fetch(table: type[T]) -> list[T]:
    name = tableDefinition(table).name
    logger.debug(f"Fetching table {name}...")
    
    filePath = getTablePath(table)
    dirPath = os.path.splitext(filePath)[0]
    objects: list[T] = []
    if os.path.isfile(filePath):
        logger.debug(f"Fetching \"{filePath}\"...")
        objects = loadFromCsv(table, filePath)
    elif os.path.isdir(dirPath):
        logger.debug(f"Fetching \"{filePath}/**.csv\"...")
        for root, dirs, files in os.walk(dirPath):
            for file in files:
                if file.endswith(".csv"):
                    objects += loadFromCsv(table, os.path.join(root, file))

    logger.info(f"Fetched {len(objects)} objects from table {name}")
    return objects


def fetchById(table: type[T], id: int) -> T | None:
    name = tableDefinition(table).name
    logger.debug(f"Fetching id {id} from table {name}...")
    objects = fetch(table)
    for o in objects:
        if getId(o, table) == id:
            logger.info(f"Found object {o} with id {id}")
            return o
    logger.info(f"Found no object with id {id}")
    return None


def delete(objects: T | list[T]) -> None:
    logger.debug(f"Deleting {objects}...")
    objectsList: list[T] = objects if type(objects) is list else [objects] # type: ignore
    objectsPerFile: dict[str, list[T]] = {}
    for i, object in enumerate(objectsList):
        logger.debug(f"{i+1}/{len(objectsList)}: Deleting {object}...")
        path = getFilePath(object)
        if path not in objectsPerFile:
            objectsPerFile[path] = loadFromCsv(type(object), path)
        objectsPerFile[path].remove(object)
        logger.debug(f"{i+1}/{len(objectsList)}: Deleted {object} from \"{path}\"")

    logger.debug(f"Saving files {objectsPerFile.keys()}...")
    for newPath, objects in objectsPerFile.items():
        saveToCsv(objects, newPath)
    logger.info(f"Deleted {objects}")


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
    logger.debug(f"Assigning new id to {object}...")
    ids = loadFromCsv(TableIds, path)
    config = tableDefinition(object)
    for line in ids:
        if line.table == config.name:
            newId = line.id = line.id + 1
            break
    else:
        ids.append(TableIds(config.name, newId := 1))

    logger.debug(f"Saving ids...")
    saveToCsv(ids, path)
    setattr(object, config.id, newId)
    logger.debug(f"Assigned id {newId} to {object}...")


_TypeAnnotation = type[Any] | str | Any
_serializers: dict[_TypeAnnotation, Callable[[Any], str]] = {}
_deserializers: dict[_TypeAnnotation, Callable[[str, _TypeAnnotation], Any]] = {}


TS = TypeVar("TS")
def setSerializer(valueType: type[TS] | _TypeAnnotation, serializer: Callable[[TS], str], deserializer: Callable[[str, type[TS] | _TypeAnnotation], TS]):
    _serializers[valueType] = serializer
    _deserializers[valueType] = deserializer
    logger.debug(f"Set serializer for type {valueType.__name__}")

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
    logger.debug(f"Saving objects {len(objects)} to \"{path}\"...")
    try:
        if len(objects) == 0:
            os.remove(path)
            logger.info(f"Removed \"{path}\"")
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            saved = 0
            logger.debug(f"Writing to \"{path}\"...")
            with open(path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=CSV_SEP)
                header = list(tableDefinition(objects[0]).fields.keys())
                writer.writerow(header)
                for i, object in enumerate(objects):
                    try:
                        logger.debug(f"{i+1}/{len(objects)}: Serializing {object}...")
                        row = [serialize(getattr(object, f)) for f in header]
                        writer.writerow(row)
                        logger.debug(f"{i+1}/{len(objects)}: Wrote {row}")
                        saved+=1
                    except Exception as e:
                        logger.error(f"{i+1}/{len(objects)}: Could not serialize object {object}: {e}")
                        logger.debug(f"{i+1}/{len(objects)}: Skipping object {object}")
            logger.info(f"Saved {saved} objects to \"{path}\"")
    except OSError as e:
        logger.error(f"Could not write {path}: {e}")
        logger.info(f"Failed to save \"{path}\"")
        return


def loadFromCsv(table: type[T], path: str) -> list[T]:
    logger.debug(f"Loading objects from \"{path}\"...")
    if not os.path.isfile(path):
        return []
    try:
        mTime = datetime.fromtimestamp(os.path.getmtime(path))
        if path in _loadedFiles and _loadedFiles[path][0] == mTime:
            logger.debug(f"File \"{path}\" was not modified since last load")
            logger.debug(f"Using {len(_loadedFiles[path][1])} cached objects from \"{path}\"")
            return _loadedFiles[path][1]

        objects: list[T] = []
        logger.debug(f"Reading from \"{path}\"...")
        with open(path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=CSV_SEP)
            fields = tableDefinition(table).fields
            header = next(reader)

            number = 1
            for row in reader:
                try:
                    logger.debug(f"{number}: Deserializing {row}...")
                    object = table(**{h: deserialize(c, fields[h]) for h, c in zip(header, row)})
                    objects.append(object)
                    logger.debug(f"{number}: Read {object}...")
                except Exception as e:
                    logger.error(f"{number}: Could not deserialize line {row}: {e}")
                    logger.debug(f"{number}: Skipping line {row}")
                number+=1

        _loadedFiles[path] = (mTime, objects)
        logger.info(f"Loaded {len(objects)} objects from \"{path}\"")
        return objects
    except OSError as e:
        print(f"[ERROR] Could not read {path}: {e}")
        logger.info(f"Failed to loaded \"{path}\"")
        return []


@dataclasses.dataclass(eq=False)
class TableIds(TableObject, name=".ids", id="table"):
    table: str
    id: int
