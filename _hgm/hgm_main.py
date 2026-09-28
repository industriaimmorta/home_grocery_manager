## Versioning Pocket #####
##########################
from typing import NamedTuple
class AppInfo(NamedTuple):
    name: str
    version: tuple[int, int, int]
    @property
    def version_string(self) -> str:
        return ".".join(map(str, self.version))

HGM = AppInfo(
    name="Home Grocery Manager",
    version=(0, 0, 2),
)

##########################

# Imports ----
### PYTHON
import json
from datetime import datetime
from pathlib import Path

class HGManager:
    def __init__(self):
        self.running = False
        self.database_dict = None
        self.time = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

        # Establish Directory Mapping
        self.install_dir = Path(__file__).resolve().parent.parent
        print(f"Found Home Directory: {self.install_dir}")
        ## TODO Module Manifest For Adjutant Plugin

        self.core_path = self.install_dir / "_hgm"
        print(f"Found Core: {self.core_path}")
        ## TODO Establish Core Functions

        self.data_path = self.install_dir / "data"
        print(f"Using Data at: {self.data_path}")
        self.database = self.data_path / "database.json"
        ## TODO Migrate to SQLite, Allow Loading Independent of [self.run]


    def run(self):
        try:
            self.validate()
            self.main_loop()
            self.close_database()

        except Exception as e:
            print(str(e)) ###DEBUG

        finally:
            self.shutdown()

    def close_database(self):
        self.data_path.mkdir(parents=True, exist_ok=True)

        with self.database.open("w", encoding="utf-8") as f:
            json.dump(self.database_dict, f, indent=4)

    def shutdown(self):
        self.running = False
        print("\n[Grocery Manager Shutdown]")

    def validate(self):
        try:
            with self.database.open("r", encoding="utf-8") as file:
                self.database_dict = json.load(file)

        except FileNotFoundError:
            print("Database is Missing! Generating new database...")

        except json.JSONDecodeError:
            print("Database is Damaged. Generating new database...")
            self.time = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
            self.database.rename(self.data_path / f"database_old_{self.time}.json")
            old_database = self.data_path / f"database_old_{self.time}.json"
            print(f"Previous Database Can be found at {old_database}")

        if not self.database.exists():
            self.database_dict = {"categories": {}}
            self.data_path.mkdir(parents=True, exist_ok=True)
            with self.database.open("w", encoding="utf-8") as f:
                json.dump(self.database_dict, f, indent=4)

    def main_loop(self):
        pass

if __name__ == "__main__":
    hgm = HGManager()
    hgm.run()