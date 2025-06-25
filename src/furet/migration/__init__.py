from dataclasses import dataclass
import importlib
import logging
import os
import re
import sys

from furet.repository import csvdb
from furet.repository.csvdb import TableObject

logger = logging.getLogger("migrations")

class Migration:
    def up(self): ...

    # def down(self): ...


@dataclass(eq=False)
class AppliedMigration(TableObject, name=".migration"):
    id: int
    migration: str

    def __str__(self):
        return self.migration


def applyMigrations():
    logger.debug("Fetching applied migrations...")
    appliedMigrationsObj = csvdb.fetch(AppliedMigration)
    if len(appliedMigrationsObj) > 0:
        logger.info(f"The last applied migration is {sorted(appliedMigrationsObj, key=lambda i: i.id)[-1]}")

    appliedMigrations = set(map(lambda m: m.migration, appliedMigrationsObj))
    missingMigrations: list[str] = []
    logger.debug("Iterating available migrations...")
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")
    for migration in  os.listdir(root):
        moduleName, ext = os.path.splitext(migration)
        if ext == ".py" and moduleName not in appliedMigrations:
            missingMigrations.append(moduleName)

    if len(missingMigrations) == 0:
        logger.info("Nothing to migrate")
        return
    
    logger.info(f"Applying {len(missingMigrations)} migrations...")

    for i, migration in enumerate(missingMigrations):
        logger.info(f"{i+1}/{len(missingMigrations)}: {migration}... ")
        match = re.match(r'(\d{4}-\d{2}-\d{2})_(.+)', migration)
        if not match:
            logger.error(f"Migration name does not match the format 'YYYY-MM-DD_<name>.py'")
            sys.exit(1)
        # date = datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
        className = match.group(2)

        module = importlib.import_module(f"furet.migration.migrations.{migration}")
        MigrationClass: type[Migration] = getattr(module, className)
        MigrationClass().up()
        csvdb.insert(AppliedMigration(0, migration=migration))
    
    logger.info(f"Successfully applied {len(missingMigrations)} migrations")
