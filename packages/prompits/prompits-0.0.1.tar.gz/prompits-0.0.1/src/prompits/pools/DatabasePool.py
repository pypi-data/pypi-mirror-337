# DatabasePool is a pool that can store and retrieve information from a database.
# DatabasePool is a subclass of Pool.
# DatabasePool is an abstract class.
# DatabasePool has practices to Query, Execute, Commit, Rollback, ListTables, ListSchemas, CreateTablee

from abc import ABC, abstractmethod
import traceback

from prompits.Schema import TableSchema
from ..Pool import Pool
from prompits.Practice import Practice
class DatabasePool(Pool, ABC):
    def __init__(self, name, description=None, connectionString=None):
        super().__init__(name, description)
        self.connectionString = connectionString
        # Add practices Query, Execute, Commit, Rollback
        self.AddPractice(Practice("Execute", self._Execute))
        self.AddPractice(Practice("Commit", self._Commit))
        self.AddPractice(Practice("Rollback", self._Rollback))


    @abstractmethod
    def _Commit(self):
        raise NotImplementedError("Commit method not implemented")

    @abstractmethod
    def _Rollback(self):
        raise NotImplementedError("Rollback method not implemented")
    

    def connect(self):
        try:
            # Implementation of connect method
            return True
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            traceback.print_exc()
            return False

    def disconnect(self):
        try:
            # Implementation of disconnect method
            return True
        except Exception as e:
            print(f"Error disconnecting from database: {str(e)}")
            traceback.print_exc()
            return False

    def execute_query(self, query):
        try:
            # Implementation of execute_query method
            return None
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            traceback.print_exc()
            return None

    def get_data(self, table_name, data):
        try:
            # Implementation of get_data method
            return []
        except Exception as e:
            print(f"Error getting data: {str(e)}")
            traceback.print_exc()
            return []

    def insert_data(self, table_name, data):
        try:
            # Implementation of insert_data method
            return False
        except Exception as e:
            print(f"Error inserting data: {str(e)}")
            traceback.print_exc()
            return False

    def update_data(self, table_name, data):
        try:
            # Implementation of update_data method
            return False
        except Exception as e:
            print(f"Error updating data: {str(e)}")
            traceback.print_exc()
            return False

    def delete_data(self, table_name, data):
        try:
            # Implementation of delete_data method
            return False
        except Exception as e:
            print(f"Error deleting data: {str(e)}")
            traceback.print_exc()
            return False