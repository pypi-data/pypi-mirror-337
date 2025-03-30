# Plaza is a service provide agents to store and retrieve data
# it is a Pit and abstract class
# it has predefiineed schema for the data that can be stored
# it has StoreAd, RetrieveAd, UpdateAd, SearchAd, DeleteAd practices

from prompits.Schema import TableSchema
from prompits.pools.DatabasePool import DatabasePool
from .Pit import Pit

class Ad:
    def __init__(self, id: str, data: dict):
        self.id = id
        self.data = data

class Plaza(Pit):
    def __init__(self, name: str, description: str, table_schema: TableSchema, pool: DatabasePool):
        super().__init__(name, description or f"Plaza {name}")
        self.set_schema(table_schema)
        self.pool = pool
        # a plaza is a table in the pool
        # check if the table exists otherwise create it
        if not self.pool.UsePractice("TableExists", self.name):
            print(f"Creating table {self.name}, schema: {self.schema.ToJson()}")
            self.pool.UsePractice("CreateTable", self.name, self.schema)

    def ToJson(self):
        return {
            "name": self.name,
            "description": self.description,
            "schema": self.schema.ToJson(),
            "pool": self.pool.ToJson()
        }
    
    def FromJson(self, json: dict):
        self.name = json["name"]
        self.description = json["description"]
        self.schema = TableSchema.FromJson(json["schema"])
        self.pool = DatabasePool.FromJson(json["pool"])
    def set_schema(self, schema: dict):
        self.schema = schema

    # Store an ad in the plaza's pool
    def StoreAd(self, table_name: str, ad: Ad):
        self.pool.Store(ad.id, ad.data)

    def RetrieveAd(self, table_name: str, id: str):
        return self.pool.Retrieve(id)

    def UpdateAd(self, table_name: str, id: str, data: dict):
        self.pool.Update(table_name, id, data)

    def SearchAd(self, table_name: str, where: dict):
        return self.pool.Search(table_name, where)

    def DeleteAd(self, id: str):
        self.pool.Delete(id)
