## Versioning Pocket #####
##########################
import os
from typing import NamedTuple
class AppInfo(NamedTuple):
    name: str
    version: tuple[int, int, int]
    @property
    def version_string(self) -> str:
        return ".".join(map(str, self.version))

HGM = AppInfo(
    name="Home Grocery Manager",
    version=(0, 1, 0),
)

##########################

# Imports ----
### PYTHON
import json
from os import system
from datetime import datetime
from pathlib import Path

class HGManager:
    def __init__(self):
        self.running = False
        self.status = None
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

    def clear(self):
        system("cls" if os.name == "nt" else "clear")

    def error(self):
        print(f"Error Completing State: {self.status}")
        print("Attempting to save database---")
        self.close_database()
        print("Returning to Main Menu")
        self.status = "main"


    def run(self, isolated):
        try:
            if isolated:
                self.validate()
                self.main_loop()
                self.close_database()
            else:
                self.validate()
                self.receive_package()
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
        self.running = True
        self.status = "main"
        while self.running:
            self.clear()
            print("\n\n----- [HOME GROCERY MANAGER] Main Menu -----\n")
            print(" ADD = Add New Item")
            print(" USE = Use an Existing Item")
            print(" LIST = Display Items Currently Available")
            print(" SHOP = Display Current Shopping List")
            print(" EXIT = Close the Program")

            user_input = input("\n> ")

            if user_input.lower() == "exit":
                break

            if user_input.lower() == "add":
                self.status = "add"
                self.add_item()

            if user_input.lower() == "use":
                self.status = "use"
                self.use_item()

            if user_input.lower() == "list":
                self.status = "list"
                self.list_database()

            if user_input.lower() == "shop":
                self.status = "shop"
                self.shopping_list()

    def add_item(self):
        try:
            self.clear()
            while self.status == "add":
                item_new = False
                located = False
                category_name = None
                print("\n\n----- [HOME GROCERY MANAGER] Add Item -----\n")
                print("Enter Item Name:\n\n\n\n")
                item_name = input("\n> ").strip().lower()
                self.clear()
                for category in self.database_dict["categories"]:
                    for item in self.database_dict["categories"][category]:
                        if item == item_name:
                            category_name = category
                            located = True
                            break
                    if category_name is not None:
                        break

                if not located:
                    print("\n\n----- [HOME GROCERY MANAGER] Add Item -----\n")
                    print("Enter Item Category:\n")
                    print("Examples: pantry, freezer, refrigerator---\n\n")
                    category_name = input("\n> ").strip().lower()
                    self.clear()

                print("\n\n----- [HOME GROCERY MANAGER] Add Item -----\n")
                if located:
                    print(f"Adding to {item_name} in {category_name}.")
                print("Enter Item Quantity to Add:\n\n\n")
                quantity = float(input("\n> "))
                self.clear()

                if category_name not in self.database_dict["categories"]:
                    self.database_dict["categories"][category_name] = {}

                if item_name not in self.database_dict["categories"][category_name]:
                    item_new = True
                    self.database_dict["categories"][category_name][item_name] = {}
                    self.database_dict["categories"][category_name][item_name]["in_house"] = quantity
                    self.database_dict["categories"][category_name][item_name]["minimum"] = 0
                    self.database_dict["categories"][category_name][item_name]["cost"] = 0

                if item_new:
                    print("\n\n----- [HOME GROCERY MANAGER] Add Item -----\n")
                    print(f"Enter Minimum of {item_name} that should be ")
                    print("on hand before adding to shopping list:\n\n")
                    quantity = float(input("\n> "))
                    self.database_dict["categories"][category_name][item_name]["minimum"] = quantity
                    self.clear()

                    print("\n\n----- [HOME GROCERY MANAGER] Add Item -----\n")
                    print(f"Enter how much {item_name} costs:\n\n\n\n")
                    cost = float(input("\n> "))
                    self.database_dict["categories"][category_name][item_name]["cost"] = cost
                    self.clear()

                if not item_new:
                    self.database_dict["categories"][category_name][item_name]["in_house"] += quantity


                print("\n\n----- [HOME GROCERY MANAGER] Add Item -----\n")
                print(f"Add another item?:\n\n\n")
                loop = (input("Enter Yes or No\n> ")).strip().lower()
                if loop == "no":
                    self.status = "main"
                if loop not in ("yes", "no"):
                    print("Unknown response. Returning to main menu.")
                    self.status = "main"

        except Exception as e:
            print("An Error Has Occurred. Returning to main menu.")
            print(str(e))
        finally:
            self.status = "main"

    def use_item(self):
        self.clear()
        while self.status == "use":
            category_name = None
            print("\n\n----- [HOME GROCERY MANAGER] Use Item -----\n")
            print("Enter Item Name:\n\n\n\n")
            item_name = input("\n> ").strip().lower()
            self.clear()
            for category in self.database_dict["categories"]:
                for item in self.database_dict["categories"][category]:
                    if item == item_name:
                        category_name = category
                        break
                if category_name is not None:
                    break

            if category_name == None:
                print("Item is not currently in the database. Returning to main menu.")
                self.status = "main"

            else:
                print("\n\n----- [HOME GROCERY MANAGER] Use Item -----\n")
                print("How much was used?\n\n\n\n")
                quantity = float(input("\n> "))
                self.clear()

                self.database_dict["categories"][category_name][item_name]["in_house"] -= quantity
                if self.database_dict["categories"][category_name][item_name]["in_house"] <= 0:
                    self.database_dict["categories"][category_name][item_name]["in_house"] = 0

                print("\n\n----- [HOME GROCERY MANAGER] Use Item -----\n")
                print(f"Use another item?:\n\n\n")
                loop = (input("Enter Yes or No\n> ")).strip().lower()
                if loop == "no":
                    self.status = "main"
                if loop not in ("yes", "no"):
                    print("Unknown response. Returning to main menu.")
                    self.status = "main"

    def list_database(self):
        self.clear()
        while self.status == "list":
            itemlist = ""
            for category in self.database_dict["categories"]:
                for item in self.database_dict["categories"][category]:
                    itemlist += f"\n{category} - {item}: {self.database_dict["categories"][category][item]["in_house"]}"

            print(itemlist)
            loop = (input("Return to Main Menu?\nYes or No\n> ")).strip().lower()
            if loop == "yes":
                self.status = "main"
            if loop not in ("yes", "no"):
                print("Unknown response. Returning to main menu.")
                self.status = "main"

    def shopping_list(self):
        self.clear()
        while self.status == "shop":
            shoplist = ""
            for category in self.database_dict["categories"]:
                for item in self.database_dict["categories"][category]:
                    item_onhand = self.database_dict["categories"][category][item]["in_house"]
                    item_min = self.database_dict["categories"][category][item]["minimum"]
                    if item_onhand <= item_min:
                        shoplist += f"\n{category} - {item}"


            print(shoplist)
            loop = (input("Return to Main Menu?\nYes or No\n> ")).strip().lower()
            if loop == "yes":
                self.status = "main"
            if loop not in ("yes", "no"):
                print("Unknown response. Returning to main menu.")
                self.status = "main"


if __name__ == "__main__":
    hgm = HGManager()
    hgm.run()