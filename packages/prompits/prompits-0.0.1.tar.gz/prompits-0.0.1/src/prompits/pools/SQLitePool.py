# SQLite is a pool of connections to a SQLite database.

from prompits.Schema import TableSchema, DataType
from ..Pool import Pool
import sqlite3
import json
import traceback
from datetime import datetime
import os
from typing import List, Any
import types
from prompits.Pool import JsonDataItem
from prompits.pools.DatabasePool import DatabasePool
from prompits.Practice import Practice


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, (types.MethodType, types.FunctionType)):
            return str(obj)  # Convert methods/functions to string representation
        elif hasattr(obj, '__dict__'):
            # Handle custom objects by converting to dict
            return {key: value for key, value in obj.__dict__.items() 
                   if not key.startswith('_') and not callable(value)}
        try:
            # Try to convert to a basic type
            return str(obj)
        except:
            # Fall back to default behavior
            return super().default(obj)


class SQLitePool(DatabasePool):
    def __init__(self, name: str, description: str, db_path: str):
        super().__init__(name, description)
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    # implement the abstract methods from the Pool class
    def _CreateTable(self, table_name: str, schema: TableSchema):
        """
        Create a table in the database.
        
        Args:
            table_name: Name of the table
            schema: TableSchema object with column definitions
            
        Returns:
            dict: Status and result information
        """
        try:
            self._ensure_connection()
            
            # Generate CREATE TABLE SQL
            column_defs = []
            for column_name, column_def in schema.rowSchema.columns.items():
                # check if column_def is a DataType
                if isinstance(column_def, dict):
                    nullable = "NOT NULL" if column_def.get("nullable", True) == False else ""
                    default = f"DEFAULT {column_def['default']}" if "default" in column_def else ""
                    data_type = column_def.get("type", DataType.STRING)
                else:
                    nullable = ""
                    default=""
                    data_type=column_def
                
                # Map data type
                sqlite_type = self._MapTypeFromDataType(data_type)
                
                column_defs.append(f"{column_name} {sqlite_type} {nullable} {default}".strip())
            
            # Add primary key
            if schema.primary_key:
                pk_columns = ", ".join(schema.primary_key)
                column_defs.append(f"PRIMARY KEY ({pk_columns})")
            
            # Build and execute the CREATE TABLE statement
            create_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(column_defs)}
                )
            """
            print(f"SQLitePool._CreateTable: {create_sql}")
            self.cursor.execute(create_sql)
            self.connection.commit()
            print(f"SQLitePool._CreateTable: {table_name} created")
            return True
        except Exception as e:
            raise sqlite3.DatabaseError(f"*** Error creating table {table_name}: {str(e)}")

    def _DropTable(self, table_name: str):
        """
        Drop a table from the database.
        
        Args:
            table_name: Name of the table
            
        Returns:
            bool: True if successful
        """
        try:
            self._ensure_connection()
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.connection.commit()
            return True
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error dropping table {table_name}: {str(e)}")
    
    def _Commit(self):
        raise NotImplementedError("SQLitePool does not support _Commit")
    
    def _Rollback(self):
        raise NotImplementedError("SQLitePool does not support _Rollback")
    

    def _ListTables(self) -> List[str]:
        """
        List all tables in the database.
        
        Returns:
            List[str]: List of table names
        """
        try:
            self._ensure_connection()
            
            # Get all tables in the database
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
            
            tables = [row[0] for row in self.cursor.fetchall()]
            
            return tables
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error listing tables: {str(e)}")
    
    def _GetTableSchema(self, table_name: str) -> TableSchema:
        """
        Get the schema of a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            TableSchema: Schema of the table
        """
        try:
            self._ensure_connection()
            
            # Check if table exists
            if not self._TableExists(table_name):
                raise sqlite3.DatabaseError(f"Table '{table_name}' does not exist")
            
            # Get table info
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            
            # Extract primary key columns
            primary_key_columns = []
            row_schema = {}
            
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = col[3] == 1
                default_value = col[4]
                is_pk = col[5] > 0
                
                if is_pk:
                    primary_key_columns.append(col_name)
                
                # Map SQLite type to DataType
                data_type = self._MapTypeToDataType(col_type)
                
                # Build column schema
                column_schema = {
                    "type": data_type,
                    "nullable": not not_null
                }
                
                if default_value is not None:
                    column_schema["default"] = default_value
                
                row_schema[col_name] = column_schema
            
            # Create TableSchema object
            schema = {
                "rowSchema": row_schema,
                "primary_key": primary_key_columns
            }
            
            return TableSchema(table_name, schema)
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error getting table schema for {table_name}: {str(e)}")
    
    def _Insert(self, table_name, data):
        """
        Insert data into a table in the database.
        
        Args:
            table_name: Name of the table
            data: Data to insert (dict or JsonDataItem)
            
        Returns:
            bool: True if inserted successfully
        """
        try:
            self._ensure_connection()
            
            # Convert JsonDataItem to dict if needed
            if isinstance(data, JsonDataItem):
                data = data.data
            
            # Handle serialization for complex types
            for key in data:
                if isinstance(data[key], (dict, list)):
                    data[key] = json.dumps(data[key], cls=DateTimeEncoder)
                elif isinstance(data[key], datetime):
                    data[key] = data[key].isoformat()
            
            # Build the INSERT statement
            columns = list(data.keys())
            placeholders = ", ".join(["?" for _ in range(len(columns))])
            values = [data[col] for col in columns]
            
            insert_sql = f"""
                INSERT INTO {table_name} ({", ".join(columns)})
                VALUES ({placeholders})
            """
            
            self.cursor.execute(insert_sql, values)
            self.connection.commit()
            
            return True
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error inserting data into {table_name}: {str(e)}")
    
    def _Update(self, table_name: str, data: dict[str, Any], where_clause: str=None, row_schema: TableSchema=None):
        """
        Update data in a table in the database.
        
        Args:
            table_name: Name of the table
            key: Key to identify the data to update
            data: Data to update
            
        Returns:
            bool: True if updated successfully
        """
        try:
            self._ensure_connection()
            
            # Convert JsonDataItem to dict if needed
            if isinstance(data, JsonDataItem):
                data = data.data
            
            # Handle serialization for complex types
            for k in data:
                if isinstance(data[k], (dict, list)):
                    data[k] = json.dumps(data[k], cls=DateTimeEncoder)
                elif isinstance(data[k], datetime):
                    data[k] = data[k].isoformat()
            
            # Build the SET part of the update statement
            set_clauses = []
            values = []
            for column in data:
                if row_schema is not None:
                    data_type = row_schema.rowSchema.columns[column]["type"]
                    data[column] = self._ConvertToDataType(data[column], data_type)
                set_clauses.append(f"{column} = ?")
                values.append(data[column])
            
            # Build the WHERE part of the update statement
            # convert where_clause to a string if it is a dict
            if where_clause and isinstance(where_clause, dict):
                where_sql, where_values = self._build_where_clause(where_clause)
            else:
                where_sql = "1=1"
            
            update_sql = f"""
                UPDATE {table_name}
                SET {", ".join(set_clauses)}
                WHERE {where_sql}
            """
            values.extend(where_values)
            print(f"SQLitePool._Update: {update_sql}")
            self.cursor.execute(update_sql, values)
            self.connection.commit()
            
            return True
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error updating data in {table_name}: {str(e)}")
    
    def _Delete(self, table_name, data_key):
        """
        Delete data from a table in the database.
        
        Args:
            table_name: Name of the table
            data_key: Key to identify the data to delete
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            self._ensure_connection()
            
            # Build where clause based on the data_key
            if isinstance(data_key, dict):
                where_sql, where_values = self._build_where_clause(data_key)
            else:
                # Assume data_key is a primary key value
                where_sql = "id = ?"
                where_values = [data_key]
            
            delete_sql = f"""
                DELETE FROM {table_name}
                WHERE {where_sql}
            """
            
            self.cursor.execute(delete_sql, where_values)
            self.connection.commit()
            
            return True
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error deleting data from {table_name}: {str(e)}")
    
    def _Execute(self, query: str, params: dict[str, Any]=None):
        """
        Execute a query on the database.
        
        Args:
            query: SQL query to execute
            params: Parameters for the query
            
        Returns:
            list: List of rows as dictionaries
        """
        try:
            self._ensure_connection()
            
            # Execute the query with parameters
            param_values = [v for v in params.values() if v is not params]
            
            if param_values:
                self.cursor.execute(query, param_values)    
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error executing query: {str(e)}") 
    

    def _Query(self, table_name: str, query: str, params: dict[str, Any]=None):
        """
        Execute a query on a specific table.
        
        Args:
            table_name: Name of the table
            query: SQL query to execute
            params: Parameters for the query
            
        Returns:
            list: List of rows as dictionaries
        """
        try:
            self._ensure_connection()
            
            # Add table name to query parameters
            query_params = params.copy() if params else {}
            query_params["table_name"] = table_name
            
            # Replace {table_name} with actual table name in query
            formatted_query = query.format(table_name=table_name)
            
            # Execute the query with parameters
            param_values = [v for v in query_params.values() if v is not params]
            
            if param_values:
                self.cursor.execute(formatted_query, param_values)
            else:
                self.cursor.execute(formatted_query)
            
            # Get column names
            column_names = [description[0] for description in self.cursor.description] if self.cursor.description else []
            
            # Fetch and convert rows to dictionaries
            rows = []
            for row in self.cursor.fetchall():
                # Convert sqlite3.Row to dict
                row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
                rows.append(row_dict)
            
            return rows
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error executing query on {table_name}: {str(e)}")
    
    def _Get(self, table_name, id_or_where=None):
        """
        Get data from a table in the database.
        
        Args:
            table_name: Name of the table
            id_or_where: ID (string) or where clause (dict), if None returns all records
            
        Returns:
            dict or list: Data from the table (single dict if ID provided, list otherwise)
        """
        try:
            self._ensure_connection()
            
            select_sql = f"SELECT * FROM {table_name}"
            values = []
            
            if id_or_where is not None:
                if isinstance(id_or_where, dict):
                    where_sql, where_values = self._build_where_clause(id_or_where)
                    select_sql += f" WHERE {where_sql}"
                    values = where_values
                else:
                    # Assume id_or_where is a primary key value
                    select_sql += " WHERE id = ?"
                    values = [id_or_where]
            
            self.cursor.execute(select_sql, values)
            
            # Get column names
            column_names = [description[0] for description in self.cursor.description]
            
            # Fetch and convert rows to dictionaries
            rows = []
            for row in self.cursor.fetchall():
                row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
                
                # Parse JSON fields
                for key, value in row_dict.items():
                    if isinstance(value, str):
                        try:
                            # Try to parse as JSON
                            if value.startswith('{') or value.startswith('['):
                                row_dict[key] = json.loads(value)
                        except:
                            pass
                
                rows.append(row_dict)
            
            if id_or_where is not None and not isinstance(id_or_where, dict):
                # Return a single row for ID queries
                return rows[0] if rows else None
            else:
                # Return all rows
                return rows
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error getting data from {table_name}: {str(e)}")
    
    def _Search(self, table_name, where):
        """
        Search for data in a table in the database.
        
        Args:
            table_name: Name of the table
            where: Where clause dictionary
                
        Returns:
            list: List of data from the table
        """
        try:
            self._ensure_connection()
            
            where_sql, where_values = self._build_where_clause(where)
            
            select_sql = f"""
                SELECT * FROM {table_name}
                WHERE {where_sql}
            """
            
            self.cursor.execute(select_sql, where_values)
            
            # Get column names
            column_names = [description[0] for description in self.cursor.description]
            
            # Fetch and convert rows to dictionaries
            rows = []
            for row in self.cursor.fetchall():
                row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
                
                # Parse JSON fields
                for key, value in row_dict.items():
                    if isinstance(value, str):
                        try:
                            # Try to parse as JSON
                            if value.startswith('{') or value.startswith('['):
                                row_dict[key] = json.loads(value)
                        except:
                            pass
                
                rows.append(row_dict)
            
            return rows
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error searching data in {table_name}: {str(e)}")
    
    def _build_where_clause(self, where):
        """
        Build a WHERE clause from a dictionary.
        
        Args:
            where: Where clause dictionary
            
        Returns:
            tuple: (where_sql, where_values)
        """
        if not where:
            return "1=1", []
        
        clauses = []
        values = []
        
        # Handle $or operator at the top level
        # both or and and are supported

        if "$or" in where:
            or_clauses = []
            for or_condition in where["$or"]:
                or_sql, or_values = self._build_where_clause(or_condition)
                or_clauses.append(f"({or_sql})")
                values.extend(or_values)
            return " OR ".join(or_clauses), values

        if "$and" in where:
            and_clauses = []
            for and_condition in where["$and"]:
                and_sql, and_values = self._build_where_clause(and_condition)
                and_clauses.append(f"({and_sql})")
                values.extend(and_values)
            return " AND ".join(and_clauses), values
        
        # Handle regular field conditions
        for field, condition in where.items():
            if field.startswith("$"):
                continue  # Skip special operators like $or already handled
                
            if condition is None:
                clauses.append(f"{field} IS NULL")
                
            elif isinstance(condition, dict):
                # Handle operators like $gt, $lt, etc.
                for op, value in condition.items():
                    if op == "$gt":
                        clauses.append(f"{field} > ?")
                        values.append(value)
                    elif op == "$lt":
                        clauses.append(f"{field} < ?")
                        values.append(value)
                    elif op == "$gte":
                        clauses.append(f"{field} >= ?")
                        values.append(value)
                    elif op == "$lte":
                        clauses.append(f"{field} <= ?")
                        values.append(value)
                    elif op == "$ne":
                        clauses.append(f"{field} != ?")
                        values.append(value)
                    elif op == "$in":
                        placeholders = ", ".join("?" for _ in value)
                        clauses.append(f"{field} IN ({placeholders})")
                        values.extend(value)
                    elif op == "$nin":
                        placeholders = ", ".join("?" for _ in value)
                        clauses.append(f"{field} NOT IN ({placeholders})")
                        values.extend(value)
                    elif op == "$like":
                        clauses.append(f"{field} LIKE ?")
                        values.append(value)
                    elif op == "$ilike":  # SQLite doesn't have ILIKE, use LIKE with COLLATE NOCASE
                        clauses.append(f"{field} LIKE ? COLLATE NOCASE")
                        values.append(value)
                    elif op == "$between":
                        clauses.append(f"{field} BETWEEN ? AND ?")
                        values.append(value[0])
                        values.append(value[1])
                    elif op == "$not":
                        # Handle nested not conditions
                        not_sql, not_values = self._build_not_condition(field, value)
                        clauses.append(not_sql)
                        values.extend(not_values)
                    elif op == "$is":
                        # Handle is condition
                        clauses.append(f"{field} IS ?")
                        values.append(value)
            else:
                clauses.append(f"{field} = ?")
                values.append(condition)
        
        return " AND ".join(clauses), values
    
    def _build_not_condition(self, field, condition):
        """
        Build a NOT condition clause.
        
        Args:
            field: Field name
            condition: Condition dict with operators
            
        Returns:
            tuple: (not_sql, not_values)
        """
        not_clauses = []
        not_values = []
        
        for op, value in condition.items():
            if op == "$like":
                not_clauses.append(f"{field} NOT LIKE ?")
                not_values.append(value)
            elif op == "$ilike":  # SQLite doesn't have ILIKE, use LIKE with COLLATE NOCASE
                not_clauses.append(f"{field} NOT LIKE ? COLLATE NOCASE")
                not_values.append(value)
            elif op == "$in":
                placeholders = ", ".join("?" for _ in value)
                not_clauses.append(f"{field} NOT IN ({placeholders})")
                not_values.extend(value)
            elif op == "$between":
                not_clauses.append(f"{field} NOT BETWEEN ? AND ?")
                not_values.append(value[0])
                not_values.append(value[1])
            elif op == "$eq":
                not_clauses.append(f"{field} != ?")
                not_values.append(value)
            elif op == "$gt":
                not_clauses.append(f"{field} <= ?")
                not_values.append(value)
            elif op == "$lt":
                not_clauses.append(f"{field} >= ?")
                not_values.append(value)
        
        return " AND ".join(not_clauses), not_values
    
    def ToJson(self):
        """
        Convert the pool to a JSON object.
        
        Returns:
            dict: JSON representation of the pool
        """
        return {
            "name": self.name,
            "description": self.description,
            "database_path": self.db_path,
            "type": "SQLitePool"
        }
    
    def _ensure_connection(self):
        """Ensure that the connection is established."""
        if not hasattr(self, 'connection') or self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.connection.cursor()
    
    def _Connect(self):
        """
        Connect to the SQLite database.
        
        Returns:
            bool: True if connected successfully
        """
        try:
            # Create directory if it doesn't exist
            db_dir = os.path.dirname(os.path.abspath(self.db_path))
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            # Connect to database
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.connection.cursor()
            self.is_connected = True
            return True
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error connecting to SQLite database: {str(e)}")
    
    def _Disconnect(self):
        """
        Disconnect from the database.
        
        Returns:
            bool: True if disconnected successfully
        """
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
                self.connection = None
                self.cursor = None
                self.is_connected = False
            return True
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error disconnecting from SQLite database: {str(e)}")
    
    def _IsConnected(self) -> bool:
        """
        Check if the pool is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return hasattr(self, 'connection') and self.connection is not None
            
    def _MapTypeFromDataType(self, data_type):
        """
        Map a DataType to a SQLite data type.
        
        Args:
            data_type: DataType to map
            
        Returns:
            str: SQLite data type
        """
        type_map = {
            DataType.INTEGER: "INTEGER",
            DataType.REAL: "REAL",
            DataType.STRING: "TEXT",
            DataType.BOOLEAN: "INTEGER",  # SQLite doesn't have a boolean type
            DataType.DATETIME: "TEXT",    # Store datetimes as ISO format strings
            DataType.JSON: "TEXT",        # Store JSON as text
            DataType.UUID: "TEXT",        # Store UUIDs as text
            DataType.ARRAY: "TEXT"       # Store arrays as JSON text
        }
        
        sqlite_type = type_map.get(data_type)
        if sqlite_type is None:
            raise NotImplementedError(f"DataType {data_type} not supported")
        return sqlite_type
    
    def _MapTypeToDataType(self, data_type):
        """
        Map a SQLite data type to a DataType.
        
        Args:
            data_type: SQLite data type to map
            
        Returns:
            DataType: Mapped DataType
        """
        # Convert to uppercase and clean up any modifiers
        clean_type = data_type.upper().split('(')[0].strip()
        
        type_map = {
            "INTEGER": DataType.INTEGER,
            "INT": DataType.INTEGER,
            "BIGINT": DataType.INTEGER,
            "REAL": DataType.FLOAT,
            "FLOAT": DataType.FLOAT,
            "DOUBLE": DataType.FLOAT,
            "TEXT": DataType.STRING,
            "VARCHAR": DataType.STRING,
            "CHAR": DataType.STRING,
            "BLOB": DataType.BINARY,
            "BOOLEAN": DataType.BOOLEAN,
            "DATE": DataType.DATE,
            "DATETIME": DataType.DATETIME,
            "TIMESTAMP": DataType.DATETIME,
        }
        
        data_type = type_map.get(clean_type)
        if data_type is None:
            raise NotImplementedError(f"SQLite type {clean_type} not supported")
        return data_type
    
    def FromJson(self, json_data):
        """
        Initialize pool from a JSON object.
        
        Args:
            json_data: JSON data to initialize from
            
        Returns:
            Pool: The initialized pool
        """
        self.name = json_data.get("name", self.name)
        self.description = json_data.get("description", self.description)
        self.db_path = json_data.get("database_path", self.db_path)
        return self
    
    def _ConvertToDataType(self, value, data_type):
        """
        Convert a Python value to the format needed for the given DataType.
        
        Args:
            value: Value to convert
            data_type: Target DataType
            
        Returns:
            The converted value
        """
        if value is None:
            return None
            
        if data_type == DataType.INTEGER:
            return int(value)
        elif data_type == DataType.FLOAT:
            return float(value)
        elif data_type == DataType.BOOLEAN:
            return 1 if value else 0  # SQLite doesn't have a boolean type
        elif data_type == DataType.DATE or data_type == DataType.DATETIME:
            if isinstance(value, datetime):
                return value.isoformat()
            return str(value)
        elif data_type == DataType.JSON or data_type == DataType.JSONB:
            if isinstance(value, (dict, list)):
                return json.dumps(value, cls=DateTimeEncoder)
            return str(value)
        elif data_type == DataType.ARRAY:
            if isinstance(value, list):
                return json.dumps(value, cls=DateTimeEncoder)
            return str(value)
        else:
            raise NotImplementedError(f"Conversion to DataType {data_type} not supported")
    
    def _ConvertFromDataType(self, data_type, value):
        """
        Convert a value from a given DataType to the appropriate Python type.
        
        Args:
            data_type: DataType of the value
            value: Value to convert
            
        Returns:
            The converted value
        """
        if value is None:
            return None
            
        if data_type == DataType.INTEGER:
            return int(value)
        elif data_type == DataType.REAL:
            return float(value)
        elif data_type == DataType.BOOLEAN:
            return bool(int(value))
        elif data_type == DataType.DATETIME:
            if isinstance(value, str):
                try:
                    return datetime.fromisoformat(value)
                except:
                    return value
            return value
        elif data_type == DataType.JSON:
            if isinstance(value, str):
                return json.loads(value)
            return value
        elif data_type == DataType.ARRAY:
            if isinstance(value, str):
                return json.loads(value)
            return value
        elif data_type == DataType.UUID:
            if isinstance(value, str):
                return uuid.UUID(value)
            return value
        elif data_type == DataType.STRING:
            return str(value)
        else:
            raise NotImplementedError(f"Conversion from DataType {data_type} not supported")
    
    def _GetTableData(self, table_name: str, id_or_where: str=None, table_schema: TableSchema=None) -> dict[str, Any]:
        """
        Get data from a table.
        
        Args:
            table_name: Name of the table
            key: Key to identify the data
            
        Returns:
            dict: Data from the table
        """
        try:
            self._ensure_connection()
            
            # Assume key is a primary key value unless it's a dict
            if id_or_where and isinstance(id_or_where, dict):
                where_sql, where_values = self._build_where_clause(id_or_where)
                select_sql = f"SELECT * FROM {table_name} WHERE {where_sql}"
                values = where_values
            elif id_or_where:
                select_sql = f"SELECT * FROM {table_name} WHERE id = ?"
                values = [id_or_where]
            else:
                select_sql = f"SELECT * FROM {table_name}"
                values = []
            print(f"SQLitePool._GetTableData: {select_sql}, \nvalues:{values}")
            self.cursor.execute(select_sql, values)
            
            # Get column names
            column_names = [description[0] for description in self.cursor.description]
            
            # Fetch and convert row to dictionary
            # Fetch all rows
            rows = []
            while True:
                row = self.cursor.fetchone()
                if not row:
                    break
                rows.append(row)
            
            rows_dict = []
            for row in rows:
                row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
                for key, value in row_dict.items():
                    if isinstance(value, str):
                        # convert value to the correct data type
                        if table_schema is not None:
                            row_dict[key] = self._ConvertFromDataType(table_schema.rowSchema.columns[key], value)
                        else:
                            try:
                                # Try to parse as JSON
                                if value.startswith('{') or value.startswith('['):
                                    row_dict[key] = json.loads(value)
                            except:
                                pass
                rows_dict.append(row_dict)

            # Parse JSON fields
            #print(f"SQLitePool._GetTableData: {rows_dict}")
            return rows_dict
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error getting data from {table_name}: {str(e)}")
    
    def _TableExists(self, table_name):
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table
            
        Returns:
            bool: True if the table exists, False otherwise
        """
        try:
            self._ensure_connection()
            
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                AND name=?
            """, (table_name,))
            
            return self.cursor.fetchone() is not None
        except Exception as e:
            raise sqlite3.DatabaseError(f"Error checking if table {table_name} exists: {str(e)}")
            
    