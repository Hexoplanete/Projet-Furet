from dataclasses import dataclass
import importlib
import os
import re
import sys

from furet.repository import csvdb
from furet.repository.csvdb import TableObject


class Migration:
    def up(self): ...

    # def down(self): ...


@dataclass(eq=False)
class AppliedMigration(TableObject, name=".migrations"):
    id: int
    migration: str

    def __str__(self):
        return self.migration


def migrate():
    appliedMigrations = set(map(lambda m: m.migration, csvdb.fetch(AppliedMigration)))
    missingMigrations: list[str] = []
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")
    for migration in  os.listdir(root):
        moduleName, ext = os.path.splitext(migration)
        if ext == ".py" and moduleName not in appliedMigrations:
            missingMigrations.append(moduleName)

    if len(missingMigrations) == 0:
        print("[INFO] Nothing to migrate")
        return
    
    print(f"[INFO] Applying {len(missingMigrations)} migrations...")

    for i, migration in enumerate(missingMigrations):
        print(f"[INFO] Running migration {migration} ({i+1}/{len(missingMigrations)}) ")
        match = re.match(r'(\d{4}-\d{2}-\d{2})_(.+)', migration)
        if not match:
            print(f"[ERROR] Migration name does not match the format 'YYYY-MM-DD_<name>.py'")
            sys.exit(1)
        # date = datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
        className = match.group(2)

        module = importlib.import_module(f"furet.migration.migrations.{migration}")
        MigrationClass: type[Migration] = getattr(module, className)
        MigrationClass().up()
        csvdb.insert(AppliedMigration(0, migration=migration))
    
    print(f"[INFO] Successfully applied {len(missingMigrations)} migrations")
