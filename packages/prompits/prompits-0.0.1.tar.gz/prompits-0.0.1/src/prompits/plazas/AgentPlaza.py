"""
Plaza module for agent communication.

A Plaza is a communication channel between agents. It allows agents to advertise
their practices and request services from other agents. It connect to a pool
and store the advertisements in a table in the pool.
"""

import threading
import time
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import traceback

# Fix circular import by importing directly from Schema module
from prompits.Schema import DataType, TableSchema
from ..Plaza import Plaza
from prompits.pools.DatabasePool import DatabasePool
from prompits.Practice import Practice
class AgentPlaza(Plaza):
    """
    AgentPlaza for agent communication.
    
    A AgentPlaza maintains a list of advertisements from agents and provides
    methods for agents to advertise, search for advertisements, and
    request services from other agents.
    """
    
    def __init__(self, name: str = "AgentPlaza", description: str = None, pool=None, table_name: str="agents", agent=None):
        """
        Initialize an AgentPlaza.
        
        Args:
            name: Name of the plaza
            description: Description of the plaza
            pool: Database pool
            table_name: Name of the table to store agent data
            agent: Reference to the owning agent
        """
        # Create the schema for the agents table
        from prompits.Schema import DataType
        
        # Define the schema for the agents table
        # contains the following columns:
        # agent_id: string
        # agent_name: string
        # status: string
        # create_time: datetime
        # update_time: datetime
        # stop_time: datetime
        # description: string
        # agent_info: json
        schema_dict = {
            "name": table_name,
            "description": "AgentPlaza",
            "primary_key": ["agent_id"],
            "rowSchema": {
                "agent_name": DataType.STRING,
                "status": DataType.STRING,
                "create_time": DataType.DATETIME,
                "update_time": DataType.DATETIME,
                "stop_time": DataType.DATETIME,
                "description": DataType.STRING,
                "agent_info": DataType.JSON,
                "agent_id": DataType.STRING
            }
        }
        table_schema = TableSchema(schema_dict)
        self.table_name = table_name
        self.agent_table_schema = table_schema
        
        # Initialize the plaza with the pool
        super().__init__(name, description or f"AgentPlaza {name}", table_schema, pool)
        
        # Set up database connection
        self.cleanup_thread = None
        self.running = False
        self.pools = [pool] if pool else []
        
        # Don't Create the table 
        # if self.pool and self.pool.TableExists(self.table_name):
        #     self.pool.DropTable(self.table_name)
            
        # Create the table if needed
        if not self.pool:
            raise ValueError("Pool is not set")
        if self.pool.UsePractice("TableExists", self.table_name):
            print(f"Table {self.table_name} already exists")
        else:
            print(f"Creating table {self.table_name}, schema: {table_schema}")
            self.pool.UsePractice("CreateTable", self.table_name, table_schema)
        
        # Add practices
        self.AddPractice(Practice("SearchAdvertisements", self.search_advertisements))
        self.AddPractice(Practice("Advertise", self.Advertise))
        self.AddPractice(Practice("AddPool", self.add_pool))
        self.AddPractice(Practice("ListActiveAgents", self.list_active_agents))
        
        # Store reference to the owning agent
        self.agent = agent
    
    def ToJson(self):
        """
        Convert the plaza to a JSON object.
        
        Returns:
            dict: JSON representation of the plaza
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": "AgentPlaza",
            "table_name": self.table_name
        }
    
    def list_active_agents(self, name_only=False, active_minutes=1):
        """
        List all active agents.
        
        Args:
            name_only: Whether to return only agent names
            
        Returns:
            list: List of active agents
        """
        # try:
            # Get all active agents from the database
        # search if stop_time is None or stop_time is 10 minutes ago
        print(f"listing active agents on {self.table_name}")
        print(f"active_minutes: {active_minutes}")
        # Use $or with two separate conditions instead of nested structure
        active_minutes_ago = datetime.now() - timedelta(minutes=active_minutes)
        agents = self.pool.UsePractice("GetTableData", self.table_name, {
            "$and": [
                {"update_time": {"$gt": active_minutes_ago}},
                {"stop_time": None}
            ]
        }, table_schema=self.agent_table_schema)
        
        # Filter out expired agents
        active_agents = []
        for agent in agents:
            # Check if the agent has expired
            #print(f"agent: {agent}")
            if agent.get("stop_time") is None:
                # Add the agent to the list of active agents
                if name_only:
                    active_agents.append(agent.get("agent_name"))
                else:
                    active_agents.append({
                        "agent_id": agent.get("agent_id"),
                        "agent_name": agent.get("agent_name"),
                        "create_time": agent.get("create_time"),
                        "update_time": agent.get("update_time"),
                        "description": agent.get("description"),
                    "agent_info": agent.get("agent_info", {})
                })
        
        return active_agents
        # except Exception as e:
        #     print(f"Error listing active agents: {str(e)}")
        #     traceback.print_exc()
        #     return []
    
    @classmethod
    def FromJson(cls, json_data: Dict[str, Any], pool=None, agent=None):
        """
        Initialize the plaza from a JSON object.
        
        Args:
            json_data: JSON object containing plaza configuration
            pool: Database pool
            agent: Reference to the owning agent
            
        Returns:
            Plaza: The initialized plaza
        """
        name = json_data.get("name", "AgentPlaza")
        description = json_data.get("description", None)
        table_name = json_data.get("table_name", "agents")
        
        return cls(name, description, pool, table_name, agent)
    
    def Advertise(self, agent_id: str, agent_name: str, description: str = None, agent_info: Dict = None):
        """
        Advertise an agent on the plaza.
        
        Args:
            agent_id: ID of the agent
            agent_name: Name of the agent
            description: Description of the agent
            agent_info: Information about the agent
            
        Returns:
            bool: True if advertised successfully, False otherwise
        """
        try:
            # Check if the agent is already advertised
            #print(f"seraching existing agent with agent_id: {agent_id}")
            existing_agent = self.pool.UsePractice("GetTableData", self.table_name, {"agent_id": agent_id})
            
            # Get the current time
            now = datetime.now()
            
            # Ensure agent_info practices are dictionaries
            #print(f"agent_info: {agent_info}")
            if agent_info and "pits" in agent_info:
                for pit_name, pit_info in agent_info["pits"].items():
                    if isinstance(pit_info, dict) and "practices" in pit_info:
                        # If practices is a list, convert it to a dictionary
                        if isinstance(pit_info["practices"], list):
                            practice_dict = {}
                            for practice in pit_info["practices"]:
                                if isinstance(practice, dict) and "name" in practice:
                                    practice_dict[practice["name"]] = practice
                            pit_info["practices"] = practice_dict
            
            # Create the agent data
            agent_data = {
                "agent_id": agent_id,
                "agent_name": agent_name,
                "description": description,
                "agent_info": agent_info,
                "update_time": now,
                "stop_time": None
            }
            
            # Update or insert the agent
            if existing_agent:
                # Update the existing agent
                self.pool.UsePractice("Update", self.table_name, agent_data, {"agent_id": agent_id})
            else:
                # Insert a new agent
                agent_data["create_time"] = now
                self.pool.UsePractice("Insert", self.table_name, agent_data)
            
            print(f"Advertised agent {agent_id} on plaza {self.name}")
            return True
        except Exception as e:
            print(f"Error advertising agent: {str(e)}")
            traceback.print_exc()
            return False
    
    def update_agent_stop_time(self, agent_id: str):
        """
        Update the stop time of an agent.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            bool: True if the update was successful, False otherwise
        """
        try:
            # Get the current time
            now = datetime.now()
            
            # Prepare the data
            data = {
                "status": "inactive",
                "stop_time": now
            }
            
            # Update the agent
            self.pool.UsePractice("Update", self.table_name, {"agent_id": agent_id}, data)
            return True
        except Exception as e:
            print(f"Error updating agent stop time: {str(e)}")
            traceback.print_exc()
            return False
    
    def start(self):
        """
        Start the plaza.
        """
        self.running = True
        
        # Start the cleanup thread
        if not self.cleanup_thread:
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop)
            self.cleanup_thread.daemon = True
            self.cleanup_thread.start()
    
    def stop(self):
        """
        Stop the plaza.
        """
        self.running = False
        
        # Wait for the cleanup thread to finish
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=1)
            self.cleanup_thread = None
    
    def remove_advertisement(self, agent_id: str):
        """
        Remove an advertisement from the plaza.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            bool: True if the removal was successful, False otherwise
        """
        try:
            self.pool.UsePractice("Delete", self.table_name, {"agent_id": agent_id})
            return True
        except Exception as e:
            print(f"Error removing advertisement: {str(e)}")
            traceback.print_exc()
            return False
    
    def search_advertisements(self, where: Dict = None):
        """
        Search for advertisements on the plaza.
        
        Args:
            where: Search criteria
            
        Returns:
            List[Dict]: List of advertisements matching the criteria
        """
        try:
            return self.pool.UsePractice("GetTableData", self.table_name, where or {})
        except Exception as e:
            print(f"Error searching advertisements: {str(e)}")
            traceback.print_exc()
            return []
    def get_agent_info(self, agent_id: str):
        """
        Get agent info from the plaza.
        """
        ad = self.get_advertisement(agent_id)
        if ad:
            return ad.get("agent_info", {})
        return None
    
    def get_advertisement(self, agent_id: str):
        """
        Get an advertisement from the plaza.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Dict: Advertisement for the agent
        """
        try:
            where = {"agent_id": agent_id}
            results = self.pool.UsePractice("GetTableData", self.table_name, where)
            if results:
                return results[0]
            return None
        except Exception as e:
            print(f"Error getting advertisement: {str(e)}")
            traceback.print_exc()
            return None
    
    def _cleanup_loop(self):
        """
        Cleanup loop to remove inactive agents.
        """
        while self.running:
            try:
                # Sleep for a while
                time.sleep(60)
                
                # TODO: Implement cleanup logic
            except Exception as e:
                print(f"Error in cleanup loop: {str(e)}")
                traceback.print_exc()
    
    def add_pool(self, pool):
        """
        Add a pool to the plaza.
        
        Args:
            pool: Pool to add
            
        Returns:
            bool: True if the pool was added successfully, False otherwise
        """
        try:
            if pool not in self.pools:
                self.pools.append(pool)
                print(f"Added pool {pool.name} to plaza {self.name}")
                
                # Connect the pool to the plaza
                if hasattr(pool, 'connect_to_plaza'):
                    pool.connect_to_plaza(self)
                    print(f"Connected pool {pool.name} to plaza {self.name}")
                
                return True
        except Exception as e:
            print(f"Error adding pool to plaza: {str(e)}")
            traceback.print_exc()
            return False

# For backward compatibility
AgentBoard = AgentPlaza 