import json
import os


class JsonDB:
    """This is my JSON database. It uses JSON to store data in tables."""

    def __init__(self, filename: str):
        self.filename: str = filename
        # Ensure the file exists with an empty dictionary
        try:
            with open(self.filename, "r") as file:
                db = json.load(file)
            if not isinstance(db, dict):
                raise ValueError(f"The content of {self.filename} is not a valid dictionary.")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            with open(self.filename, "w") as file:
                json.dump({}, file, indent=4)

    def create_table(self, table_name: str):
        """Add a new table to the database."""
        with open(self.filename, "r") as file:
            db = json.load(file)

        if table_name not in db:
            db[table_name] = []  # Initialize the table with an empty list

        with open(self.filename, "w") as file:
            json.dump(db, file, indent=4)
        return self

    def add_data(self, table_name: str, **data):
        """Add a new record to a specific table."""
        with open(self.filename, "r") as file:
            db = json.load(file)

        if table_name not in db:
            db[table_name] = []

        db[table_name].append(data)

        with open(self.filename, "w") as file:
            json.dump(db, file, indent=4)
        
        return self

    def delete_data(self, table_name: str, index: int) -> tuple[str, bool]:
        """Delete a record by its index from a specific table."""
        with open(self.filename, "r") as file:
            db = json.load(file)

        try:
            if table_name not in db:
                return f"Table '{table_name}' does not exist", False
            db[table_name].pop(index)
        except IndexError:
            return f"Data at index {index} does not exist", False

        with open(self.filename, "w") as file:
            json.dump(db, file, indent=4)
        
        return f"Data at index {index} deleted from table '{table_name}'", True

    def update_data(self, table_name: str, index: int, **new_data) -> tuple[str, bool]:
        """Update a specific record in the table by its index."""
        with open(self.filename, "r") as file:
            db = json.load(file)

        try:
            if table_name not in db:
                return f"Table '{table_name}' does not exist", False
            if index < 0 or index >= len(db[table_name]):
                return f"Data at index {index} does not exist in table '{table_name}'", False

            # Update the existing data with new data
            db[table_name][index].update(new_data)
        except IndexError:
            return f"Data at index {index} does not exist", False

        with open(self.filename, "w") as file:
            json.dump(db, file, indent=4)

        return f"Data at index {index} updated successfully in table '{table_name}'", True

    def get_data(self, table_name: str) -> list:
        """Retrieve all data from a specific table."""
        with open(self.filename, "r") as file:
            db = json.load(file)

        if table_name not in db:
            return []

        return db[table_name]

    def exists(self, table_name: str, **data) -> bool:
        """Check if a specific record exists in the table."""
        with open(self.filename, "r") as file:
            db = json.load(file)

        if table_name not in db:
            return False

        for record in db[table_name]:
            if all(record.get(k) == v for k, v in data.items()):
                return True
        return False

    def get_data_by(self, search_key: str, search_value):
        """
        Retrieve all records matching a specific key-value pair.

        :param search_key: The key to search for (e.g., 'name').
        :param search_value: The value to match (e.g., 'Alice').
        :return: List of matching records.
        """
        with open(self.filename, "r") as file:
            db = json.load(file)

        matching_records = []
        for table in db.values():  # Iterate through all tables
            for record in table:  # Iterate through records
                if record.get(search_key) == search_value:  # Check for matching key-value
                    matching_records.append(record)

        return matching_records

    def update_data(self, table_name: str, key: str, old_value, new_value):
        """
        Update the value of a specific key in the record of the specified table.
        
        :param table_name: The table to update (e.g., 'users').
        :param key: The key whose value needs to be updated.
        :param old_value: The current value of the key to be replaced.
        :param new_value: The new value to set for the key.
        """
        with open(self.filename, "r") as file:
            db = json.load(file)

        # Check if the table exists
        if table_name not in db:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Find the record and update it
        updated = False
        for record in db[table_name]:
            if record.get(key) == old_value:
                record[key] = new_value
                updated = True
                break

        if not updated:
            raise ValueError(f"Record with {key} = {old_value} not found in table '{table_name}'.")

        # Save the updated data
        with open(self.filename, "w") as file:
            json.dump(db, file, indent=4)

        return self

    def delete_table(self, table_name: str):
        """Delete all data in a specific table."""
        with open(self.filename, 'r') as file:
            db = json.load(file)
        
        if table_name in db:
            db[table_name] = []  # Clear all data in the table

        with open(self.filename, 'w') as file:
            json.dump(db, file, indent=4)
        return f"All data in '{table_name}' table has been deleted."
    
    def get_all_data(self):
        with open(self.filename, 'r') as file:
            db = json.load(file)
        return db
    
    def delete_all(self):
        with open(self.filename, 'w') as file:
            json.dump({}, file)

        return True
    
    def delete_db(self):
        os.remove(self.filename)
        return True
