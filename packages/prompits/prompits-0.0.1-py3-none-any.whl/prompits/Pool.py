"""
Pool module for data storage and retrieval.

A Pool is a data storage and retrieval system that can be used by agents.
It provides methods for storing, retrieving, updating, and deleting data.
"""

import uuid
import json
import threading
import time
from abc import abstractmethod, ABC
from typing import Dict, List, Any, Optional, Tuple, Union
from .Pit import Pit
from .Schema import DataType, TableSchema
from .Practice import Practice
from datetime import datetime

# DataItem is an abstract class that defines the data item in Pool
class DataItem(ABC):
    def __init__(self, id: str, name: str, description: str, data_type: DataType):
        self.id = id
        self.name = name
        self.description = description
        self.data_type = data_type
        self.created_at = time.time()
        self.updated_at = time.time()

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataItem':
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, json_str: str) -> 'DataItem':
        pass

# TextDataItem is a data item that contains text
class TextDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: str):
        super().__init__(id, name, description, DataType.STRING)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=data.get("data", "")
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'TextDataItem':
        return cls.from_dict(json.loads(json_str))

# IntegerDataItem is a data item that contains an integer
class IntegerDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: int):
        super().__init__(id, name, description, DataType.INTEGER)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IntegerDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=data.get("data", 0)
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'IntegerDataItem':
        return cls.from_dict(json.loads(json_str))

# RealDataItem is a data item that contains a floating point number
class RealDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: float):
        super().__init__(id, name, description, DataType.REAL)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RealDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=data.get("data", 0.0)
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'RealDataItem':
        return cls.from_dict(json.loads(json_str))

# ObjectDataItem is a data item that contains an object
class ObjectDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: Dict[str, Any]):
        super().__init__(id, name, description, DataType.OBJECT)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ObjectDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=data.get("data", {})
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'ObjectDataItem':
        return cls.from_dict(json.loads(json_str))

# BooleanDataItem is a data item that contains a boolean
class BooleanDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: bool):
        super().__init__(id, name, description, DataType.BOOLEAN)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BooleanDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=data.get("data", False)
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'BooleanDataItem':
        return cls.from_dict(json.loads(json_str))

# DateTimeDataItem is a data item that contains a datetime
class DateTimeDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: float):
        super().__init__(id, name, description, DataType.DATETIME)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DateTimeDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=data.get("data", time.time())
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'DateTimeDataItem':
        return cls.from_dict(json.loads(json_str))

# TupleDataItem is a data item that contains a tuple
class TupleDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: Tuple):
        super().__init__(id, name, description, DataType.ARRAY)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": list(self.data),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TupleDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=tuple(data.get("data", ()))
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'TupleDataItem':
        return cls.from_dict(json.loads(json_str))

# JsonDataItem is a data item that contains a json object
class JsonDataItem(DataItem):
    def __init__(self, id: str, name: str, description: str, data: Union[Dict[str, Any], List[Any]]):
        super().__init__(id, name, description, DataType.JSON)
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.data_type.value,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JsonDataItem':
        item = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            data=data.get("data", {})
        )
        if "created_at" in data:
            item.created_at = data["created_at"]
        if "updated_at" in data:
            item.updated_at = data["updated_at"]
        return item

    @classmethod
    def from_json(cls, json_str: str) -> 'JsonDataItem':
        return cls.from_dict(json.loads(json_str))

# Pool is a class that stores data items
class Pool(Pit):
    """
    A pool for storing data items.
    """
    
    def __init__(self, name: str, description: str = None):
        """
        Initialize a Pool.
        
        Args:
            name: Name of the pool
            description: Description of the pool
        """
        super().__init__(name, description or f"Pool {name}")
        self.data = {}
        self.lock = threading.Lock()
        self.board = None
        self.AddPractice(Practice("MapTypeFromDataType", self._MapTypeFromDataType))
        self.AddPractice(Practice("MapTypeToDataType", self._MapTypeToDataType))
        self.is_connected=False
        self.AddPractice(Practice("Connect", self._Connect))
        self.AddPractice(Practice("Disconnect", self._Disconnect))
        self.AddPractice(Practice("IsConnected", self._IsConnected))
        self.AddPractice(Practice("CreateTable", self._CreateTable))
        self.AddPractice(Practice("DropTable", self._DropTable))
        self.AddPractice(Practice("ListTables", self._ListTables))
        self.AddPractice(Practice("GetTableSchema", self._GetTableSchema))
        self.AddPractice(Practice("Insert", self._Insert))
        self.AddPractice(Practice("Update", self._Update))
        self.AddPractice(Practice("Delete", self._Delete))
        self.AddPractice(Practice("Query", self._Query))
        self.AddPractice(Practice("GetTableData", self._GetTableData))
        self.AddPractice(Practice("ConvertToDataType", self._ConvertToDataType))
        self.AddPractice(Practice("ConvertFromDataType", self._ConvertFromDataType))
        self.AddPractice(Practice("SupportedDataType", self._SupportedDataType))
        self.AddPractice(Practice("TableExists", self._TableExists))

    @abstractmethod
    def _CreateTable(self, table_name: str, schema: TableSchema):
        """
        Create a table in the pool.
        """
        raise NotImplementedError("CreateTable not implemented")

    @abstractmethod
    def _DropTable(self, table_name: str):
        """
        Drop a table in the pool.
        """
        raise NotImplementedError("DropTable not implemented")

    @abstractmethod
    def _ListTables(self) -> List[str]:
        """
        List all tables in the pool.
        """
        raise NotImplementedError("ListTables not implemented")

    @abstractmethod
    def _GetTableSchema(self, table_name: str) -> TableSchema:
        """
        Get the schema of a table in the pool.
        """
        raise NotImplementedError("GetTableSchema not implemented")

    @abstractmethod
    def _Insert(self, table_name: str, data: dict[str, Any]):
        """
        Insert data into a table in the pool.
        """
        raise NotImplementedError("Insert not implemented")

    @abstractmethod
    def _Update(self, table_name: str, key: str, data: dict[str, Any]):
        """
        Update data in a table in the pool.
        """
        raise NotImplementedError("Update not implemented")

    @abstractmethod
    def _Delete(self, table_name: str, key: str):
        """
        Delete data from a table in the pool.
        """
        raise NotImplementedError("Delete not implemented")

    @abstractmethod
    def _Query(self, table_name: str, query: str, params: dict[str, Any]):
        """
        Query data from a table in the pool.
        """
        raise NotImplementedError("Query not implemented")

    @abstractmethod
    def _GetTableData(self, table_name: str, key: str) -> dict[str, Any]:
        """
        Get data from a table in the pool.
        """
        raise NotImplementedError("GetTableData not implemented")

    @abstractmethod
    def _TableExists(self, table_name: str) -> bool:
        """
        Check if a table exists in the pool.
        """
        raise NotImplementedError("TableExists not implemented")

    @abstractmethod
    def _Connect(self):
        """
        Connect to the pool.
        """
        raise NotImplementedError("Connect not implemented")
    
    @abstractmethod
    def _Disconnect(self):
        """
        Disconnect from the pool.
        """
        raise NotImplementedError("Disconnect not implemented") 

    @abstractmethod
    def _IsConnected(self) -> bool:
        """
        Check if the pool is connected.
        """
        return self.is_connected    
    
    @abstractmethod
    def _MapTypeFromDataType(self, data_type: DataType) -> str:
        """
        Map a DataType to pool's data type.
        """
        raise NotImplementedError("MapTypeFromDataType not implemented")

    @abstractmethod
    def _MapTypeToDataType(self, data_type: str) -> DataType:
        """
        Map a pool's data type to a DataType.
        """
        raise NotImplementedError("MapTypeToDataType not implemented")

    @abstractmethod
    def _ConvertToDataType(self, data: Any) -> DataType:
        """
        Convert data to a DataType.
        """
        raise NotImplementedError("ConvertToDataType not implemented")

    @abstractmethod
    def _ConvertFromDataType(self, data_type: DataType, data: Any) -> Any:
        """
        Convert data from a DataType to a Python object.
        """
        raise NotImplementedError("ConvertFromDataType not implemented")

    def _SupportedDataType(self) -> List[DataType]:
        """
        Return a list of supported DataType by checking MapTypeFromDataType.
        
        Returns:
            List[DataType]: List of supported DataType
        """
        supported_types = []
        for data_type in DataType:
            try:
                self.MapTypeFromDataType(data_type)
                supported_types.append(data_type)
            except NotImplementedError:
                pass
            except ValueError:
                pass
        return supported_types

    @abstractmethod
    def ToJson(self):
        """
        Convert the pool to a JSON object.
        
        Returns:
            dict: JSON representation of the pool
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }

    @abstractmethod
    def FromJson(self, json_data):
        """
        Initialize the pool from a JSON object.
        
        Args:
            json_data: JSON object containing pool configuration
            
        Returns:
            Pool: The initialized pool
        """
        self.name = json_data.get("name", self.name)
        self.description = json_data.get("description", self.description)
        return self
    
    
class MemoryPool(Pool):
    """
    A memory-based pool for storing data items.
    """
    
    def __init__(self, name: str, description: str = None):
        """
        Initialize a MemoryPool.
        
        Args:
            name: Name of the pool
            description: Description of the pool
        """
        super().__init__(name, description)
        # Data is already initialized in the parent class
    
    # All methods are inherited from the parent class
