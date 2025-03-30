# Agent is a Pit and can host multiple pits.
# Agent's practices are the practices of the pits it hosts and it can use the practices of the pits it hosts.
# Agent is a software can be instantiated on a machine.
# Agent can communicate with other agents through multiple communication channels called Plug
# Agent can send and receive messages through plugs

# Agent can be described as a JSON object ToJson()
# Agent can be initialized from a JSON object __init__(json)
# Json contains environments (os, cpu, gpu, memory, etc.)
# Sample JSON:
# {
#     "name": "Agent1",
#     "description": "Agent1 description",
#     "pits": [
#         {
#             "name": "Pit1",
#             "description": "Pit1 description"
#         }
#     ],
#     "plugs": [
#         {
#             "name": "Plug1",
#             "description": "Plug1 description"
#         }
#     ],
#     "environments": {
#         "os": "Linux",
#         "cpu": {
#             "model": "Intel Core i7",
#             "cores": 8,
#             "threads": 16,
#             "frequency": 3.5
#         },
#         "gpu": {
#             "model": "NVIDIA GeForce RTX 3070",
#             "memory": 8192,
#             "cores": 24,
#             "frequency": 1.7
#         },
#         "memory": {
#             "total": 16384,
#             "free": 8192
#         }
#     }
# }

from multiprocessing import Pool
import platform
import uuid
import psutil
import threading
import time
import json
import importlib
import os
import sys
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
import traceback

from prompits.Plaza import Plaza
from prompits.Practice import Practice
from prompits.messages.UsePracticeMessage import UsePracticeRequest, UsePracticeResponse
from prompits.plazas import AgentPlaza
from prompits.plugs.gRPCPlug import gRPCPlug
from prompits.services.APIService import APIService
from prompits.services.JobMarket import JobMarket
# Remove the circular import
# from prompits.messages import UsePracticeMessage

from .Message import Message
from .Plug import Plug
from .Pit import Pit
from .Pool import Pool
from .pools.DatabasePool import DatabasePool
from .AgentAddress import AgentAddress

class AgentInfo:
    def __init__(self, agent_name: str="Agent", description: str = None, agent_id: str = None,
                 environments={}, plugs={}, pools={}, plazas={}, services={}):
        self.agent_name = agent_name
        self.description = description
        self.agent_id = agent_id
        self.plugs: Dict[str, Plug] = plugs
        self.pools: Dict[str, Pool] = pools
        self.plazas: Dict[str, Plaza] = plazas
        self.services: Dict[str, APIService] = services
        self.environments = environments

    def ToJson(self):

        return {
            "agent_name": self.agent_name,
            "description": self.description,
            "agent_id": self.agent_id,
            "components": {
                "plugs": {plug.name: plug.ToJson() for plug in self.plugs.values()},
                "pools": {pool.name: pool.ToJson() for pool in self.pools.values()},
                "plazas": {plaza.name: plaza.ToJson() for plaza in self.plazas.values()},
                "services": {service.name: service.ToJson() for service in self.services.values()}
            },
            "environments": self.environments
        }
    # create a class method to create an AgentInfo object from a JSON object
    @classmethod
    def FromJson(cls, json: dict):
        return cls(
            agent_name=json.get("agent_name"),
            description=json.get("description"),
            agent_id=json.get("agent_id"),
            environments=json.get("environments", {}),
            plugs=json.get("components", {}).get("plugs", {}),
            pools=json.get("components", {}).get("pools", {}),
            plazas=json.get("components", {}).get("plazas", {}),
            services=json.get("components", {}).get("services", {})
        )
        
        components = json.get("components", {})
        self.plugs = components.get("plugs", {})
        self.pools = components.get("pools", {})
        self.plazas = components.get("plazas", {})
        self.services = components.get("services", {})

class Agent(Pit):
    def __init__(self, name: str="Agent", description: str = None, agent_id: str = None):
        """
        Initialize an Agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent
            agent_id: Optional ID for the agent, will generate a new UUID if not provided
        """
        super().__init__(name, description)
        self.agent_id = agent_id if agent_id else str(uuid.uuid4())
        self.plugs : dict[str, Plug] = {}
        self.pools : dict[str, Pool] = {}
        self.services : dict[str, APIService] = {}
        self.plazas : dict[str, Plaza] = {}
        self.owned_plazas : dict[str, Plaza] = {}
        self.connected_plazas : dict[str, Plaza] = {}
        self.running = False
        self.advertisement_threads = {}
        self.environments = self.detect_environments()
        self.message_handler = None
        self.peer_list = {}  # Dictionary to store peer information
        self.refresh_thread = None  # Thread for refreshing advertisements
        self.refresh_stop_event = None  # Event to signal the refresh thread to stop
        
        # Add agent practices
        self.AddPractice(Practice("ListPits", self.ListPits))
        self.AddPractice(Practice("StopAgent", self.StopAgent))
        self.AddPractice(Practice("RefreshPractice", self.RefreshPractice))
        self.AddPractice(Practice("SendMessage", self.SendMessage))
        self.AddPractice(Practice("ReceiveMessage", self.ReceiveMessage))
        self.AddPractice(Practice("Advertise", self.Advertise))
        peer_list = []

    # self.pits is a property that returns a dictionary of plugs, pools, plazas, services
    @property
    def pits(self):
        return {
            "plugs": self.plugs,
            "pools": self.pools,
            "plazas": self.plazas,
            "services": self.services
        }

    # ListPits returns a list of pits
    def ListPits(self, name_only=False):
        result=[]
        if name_only:
            for pit_type, pit_type_dict in self.pits.items():
                for pit_name, pit in pit_type_dict.items():
                    result.append(pit_name)
        else:
            for pit_type, pit_type_dict in self.pits.items():
                for pit_name, pit in pit_type_dict.items():
                    result.append(pit)
        return result
    
    #@classmethod
    def create_component(self, component_type: str, component_config: Dict[str, Any]):
        """
        Create a component from a configuration.
        
        Args:
            component_type: Type of component to create
            component_config: Configuration for the component
            
        Returns:
            The created component
        """
        # Get component name and description
        name = component_config.get("name", component_type)
        description = component_config.get("description", f"{component_type} {name}")
        
        # Create a copy of the config without name and description
        config_copy = component_config.copy()
        if "name" in config_copy:
            del config_copy["name"]
        if "description" in config_copy:
            del config_copy["description"]
        if "type" in config_copy:
            del config_copy["type"]
            
        print(f"Creating component {component_type} with name {name} and description {description}")
        # Handle special cases for component types
        if component_type == "PostgresPool":
            # PostgresPool requires connection_string as a positional argument
            connection_string = config_copy.get("connection_string")
            if "connection_string" in config_copy:
                del config_copy["connection_string"]
                
            # Import the component class
            try:
                from prompits.pools.PostgresPool import PostgresPool
                component_class = PostgresPool
            except ImportError:
                print(f"Error importing PostgresPool: {str(e)}")
                return None
                
            # Create the component
            try:
                component = component_class(name, description, connection_string, **config_copy)
                return component
            except Exception as e:
                print(f"Error creating component {component_type} with name {name}: {str(e)}")
                traceback.print_exc()
                return None
        elif component_type == "SQLitePool":
            # SQLitePool requires database_path as a positional argument
            database_path = config_copy.get("database_path", config_copy.get("connection_string"))
            if "database_path" in config_copy:
                del config_copy["database_path"]
            if "connection_string" in config_copy:
                del config_copy["connection_string"]
                
            # Import the component class
            try:
                from prompits.pools.SQLitePool import SQLitePool
                component_class = SQLitePool
            except ImportError as e:
                print(f"Error importing SQLitePool: {str(e)}")
                return None
                
            # Create the component
            try:
                component = component_class(name, description, database_path, **config_copy)
                return component
            except Exception as e:
                print(f"Error creating component {component_type} with name {name}: {str(e)}")
                traceback.print_exc()
                return None
        elif component_type == "TCPPlug":
            # Import the component class
            try:
                from prompits.plugs.TCPPlug import TCPPlug
                component_class = TCPPlug
            except ImportError as e:
                print(f"Error importing TCPPlug: {str(e)}")
                return None
                
            # Create the component
            try:
                component = component_class(name, description, **config_copy)
                return component
            except Exception as e:
                print(f"Error creating component {component_type} with name {name}: {str(e)}")
                traceback.print_exc()
                return None
        elif component_type == "gRPCPlug":
            # Import the component class
            try:
                from prompits.plugs.gRPCPlug import gRPCPlug
                component_class = gRPCPlug
            except ImportError as e:
                print(f"Error importing gRPCPlug: {str(e)}")
                return None
                
            # Create the component
            try:
                component = component_class(name, description, **config_copy)
                return component
            except Exception as e:
                print(f"Error creating component {component_type} with name {name}: {str(e)}")
                traceback.print_exc()
                return None
        elif component_type == "AgentPlaza":
            # Import the component class
            try:
                from prompits.plazas.AgentPlaza import AgentPlaza
                component_class = AgentPlaza
                config_copy["pool"] = self.pools[component_config["pool"]]
                #print(f"Imported AgentPlaza {component_config}")
            except ImportError as e:
                print(f"Error importing AgentPlaza: {str(e)}")
                return None
        elif component_type=="Ollama":
            # Import the component class
            try:
                print(f"Importing Ollama")
                from prompits.services.Ollama import Ollama
                component_class = Ollama
            except ImportError as e:
                print(f"Error importing Ollama: {str(e)}")
                return None
        elif component_type=="JobMarket":
            # Import the component class
            try:
                print(f"Importing JobMarket")
                from prompits.services.JobMarket import JobMarket
                component_class = JobMarket
            except ImportError as e:
                print(f"Error importing JobMarket: {str(e)}")
                return None
        else:
            print(f"Unknown component type: {component_type}")
            return None
        
            # Create the component
        try:
            component = component_class(name, description, **config_copy)
            return component
        except Exception as e:
            print(f"Error creating component {component_type} with name {name}: {str(e)}")
            traceback.print_exc()
            return None

    # create a class method to initialize an agent from an AgentInfo object and return an Agent object
    @classmethod
    def FromJson(cls, agent_info: AgentInfo, quiet_mode: bool = False):
        """
        Initialize an agent from an AgentInfo object.
        
        Args:
            agent_info: AgentInfo object containing agent information
            quiet_mode: Whether to suppress output messages

        Returns:
            Agent: The initialized agent
        """
        if not isinstance(agent_info, AgentInfo):
            raise TypeError("agent_info must be an AgentInfo object")
        
        # Set agent name and description
        agent = cls(agent_info.agent_name, agent_info.description)
        
        # Override agent_id if specified
        if agent_info.agent_id:
            agent.agent_id = agent_info.agent_id
            
        # Set environments
        agent.environments = agent_info.environments
        
        # Process plugs
        for plug_name, plug in agent_info.plugs.items():
            # create the plug
            agent.plugs[plug_name] = agent.create_component(plug["type"], plug)
            if not quiet_mode:
                print(f"Added plug {plug_name} to agent {agent.name}")
        
        # Process services
        for service_name, service in agent_info.services.items():
            # create the service
            agent.services[service_name] = agent.create_component(service["type"], service)
            if not quiet_mode:
                print(f"Added service {service_name} to agent {agent.name}")
                
            # If service is a JobMarket and has a pool_name, set the pool
            if isinstance(service, JobMarket) and hasattr(service, "pool_name") and service.pool_name:
                pool_name = service.pool_name
                if pool_name in agent.pools:
                    service.set_pool(agent.pools[pool_name])
                    if not quiet_mode:
                        print(f"Set pool {pool_name} for service {service_name}")
                else:
                    print(f"Warning: Pool {pool_name} not found for service {service_name}")
        
        # Process pools
        for pool_name, pool in agent_info.pools.items():
            # create the pool
            agent.pools[pool_name] = agent.create_component(pool["type"], pool)
            if not quiet_mode:
                print(f"Added pool {pool_name} to agent {agent.name}")
        
        # Process plazas
        for plaza_name, plaza in agent_info.plazas.items():
            # create the plaza
            print(f"Creating plaza {plaza_name} with type {plaza['type']}")
            print(f"plaza: {plaza}")
            agent.plazas[plaza_name] = agent.create_component(plaza["type"], plaza)
            print(f"plaza created: {agent.plazas[plaza_name]}")
            if isinstance(agent.plazas[plaza_name], AgentPlaza):
                #self.create_plaza(plaza_name, plaza)
                print(f"plaza pool: {plaza['pool']}")
                agent.plazas[plaza_name].pool = agent.pools[plaza['pool']]
                if not quiet_mode:
                    print(f"Created plaza {plaza_name}")
            else:
                raise ValueError(f"Unknown plaza type: {type(plaza)}")
        
        # Add plaza practices to the agent
        for plaza_name, plaza in agent.plazas.items():
            # Add plaza practices to the agent
            for practice_name, practice_func in plaza.practices.items():
                # Create a closure to capture the plaza and practice_name
                def create_plaza_practice_func(plaza_obj, practice_name_str):
                    return lambda *args, **kwargs: getattr(plaza_obj, practice_name_str)(*args, **kwargs)
                
                agent.AddPractice(Practice(f"{plaza_name}/{practice_name}", create_plaza_practice_func(plaza, practice_name)))
                if not quiet_mode:
                    print(f"Added plaza practice {plaza_name}/{practice_name} to agent {agent.name}")
        
        # Add pool practices to the agent
        for type_name, type_dict in agent.pits.items():
            print(f"adding practices type_name: {type_name}")
            for pit_name, pit in type_dict.items():
                if hasattr(pit, 'practices'):
                    print(f"adding practices pit_name: {pit_name}")
                    for practice_name, practice_func in pit.practices.items():
                        # Create a closure to capture the pit and practice_name
                        def create_pit_practice_func(pit_obj, practice_name_str):
                            return lambda *args, **kwargs: getattr(pit_obj, practice_name_str)(*args, **kwargs)
                        
                        agent.AddPractice(Practice(f"{pit_name}/{practice_name}", create_pit_practice_func(pit, practice_name)))
                        if not quiet_mode:
                            print(f"Added pool practice {pit_name}/{practice_name} to agent {agent.name}")
        
        return agent

    def to_AgentInfo(self):
        return AgentInfo(
            agent_id=self.agent_id,
            agent_name=self.name,
            description=self.description,
            environments=self.environments,
            plugs=self.plugs,
            pools=self.pools,
            plazas=self.plazas,
            services=self.services
        )

    def ToJson(self):
        return self.to_AgentInfo().ToJson()

    def request_use_practice(self, to_agent: str, practice: str, **kwargs):
        """
        Request to use a practice from another agent.
        
        Args:
            to_agent: The agent to request the practice from
            practice: The practice to request
            **kwargs: Additional arguments for the practice
            
        Returns:
            bool: True if the practice was requested successfully, False otherwise
        """
        # send a UsePracticeMessage to the other agent
        message = UsePracticeMessage(self.agent_id, to_agent, practice, **kwargs)
        self.send_message(message, [to_agent])

    def detect_environments(self):
        """
        Detect environments from the host machine.
        
        Returns:
            dict: Environment information
        """
        # Get CPU information
        cpu_info = {
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "percent": psutil.cpu_percent()
        }
        
        # Get memory information
        memory = psutil.virtual_memory()
        memory_info = {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent
        }
        
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu": cpu_info,
            "memory": memory_info
        }

    def SendMessage(self, message: Message, recipients: List[AgentAddress]):
        """
        Send a message to other agents.
        
        Args:
            message: The message to send
            recipients: List of AgentAddress objects
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        for recipient in recipients:
            # solve the address and send the message
            # check if recipient is in self.peer_list
            # if not in self.peer_list, Advertise the agent to the plaza and check again
            if isinstance(recipient, str):
                recipient = AgentAddress(recipient.split('@')[0], recipient.split('@')[1])
                recipient_string = recipient.to_string()
            elif isinstance(recipient, dict):
                recipient_string = recipient['agent_id']+'@'+recipient['plaza_name']
                recipient = AgentAddress(recipient['agent_id'], recipient['plaza_name'])
            else:
                recipient_string = recipient.to_string()
            
            if recipient.to_string() not in self.peer_list.keys():
                self.Advertise(recipient.plaza_name)
                if recipient.to_string() not in self.peer_list.keys():
                    raise ValueError(f"Recipient {recipient} not found in peer list")
            if recipient.to_string() in self.peer_list.keys():
                # find available plug for the recipient
                #print(f"agent_info: {self.peer_list[recipient.to_string()]['agent_info']['components'].keys()}")
                plugs_info = self.peer_list[recipient.to_string()]['agent_info']['components']['plugs']
                for plug_info in plugs_info:
                    #print(f"plug_info: {plug_info}")
                    #print(f"plugs_info[plug_info]: {plugs_info[plug_info]}")
                    if "type" in plugs_info[plug_info]:
                        if plugs_info[plug_info]['type'] == 'gRPCPlug':
                            # create a gRPCPlug object to connect to the recipient
                            address={"host": plugs_info[plug_info]['host'], "port": plugs_info[plug_info]['port']}
                            plug = gRPCPlug(address["host"], address["port"])
                            if plug.SendMessage(recipient, message, address):
                                return True
                        else:
                            raise ValueError(f"Unsupported plug type: {plugs_info[plug_info]['type']}")
                    else:   
                        raise ValueError(f"No plug type: {plug_info}")
            else:
                print(f"Peer list: {self.peer_list.keys()}")
                raise ValueError(f"Recipient {recipient} not found in peer list")

    def ReceiveMessage(self, msg_count: int = 0):
        """
        Receive a message from another agent.
        
        Args:
            msg_count: int, number of messages to receive. 0 means all messages.
        Returns:
            list[Message]: list of messages
        """
        msg_list:[Message] = []
        # receive messages from all plugs
        for plug in self.plugs.values():
            msg_list.extend(plug.UsePractice("ReceiveMessage", msg_count))
        return msg_list
        

    def remove_pit(self, pit_name: str):
        """
        Remove a pit from the agent.
        
        Args:
            pit_name: Name of the pit
            
        Returns:
            bool: True if the pit was removed successfully, False otherwise
        """
        # check if pit_name is in self.plugs, self.pools, self.plazas, self.services
        if pit_name in self.plugs:
            del self.plugs[pit_name]
        elif pit_name in self.pools:
            del self.pools[pit_name]
        elif pit_name in self.plazas:
            del self.plazas[pit_name]
        elif pit_name in self.services:
            del self.services[pit_name]
        else:
            print(f"Pit {pit_name} does not exist")
            return False
        print(f"Removed pit {pit_name} from agent {self.name}")
        return True

    def get_pit(self, pit_name: str):
        """
        Get a pit by name.
        
        Args:
            pit_name: Name of the pit
            
        Returns:
            object: The pit, or None if not found   
        """
        # check if pit_name is in self.plugs, self.pools, self.plazas, self.services
        if pit_name in self.plugs:
            return self.plugs[pit_name]
        elif pit_name in self.pools:
            return self.pools[pit_name]
        elif pit_name in self.plazas:
            return self.plazas[pit_name]
        elif pit_name in self.services:
            return self.services[pit_name]
        else:
            print(f"Pit {pit_name} does not exist")
            return None

    def create_plaza(self, plaza_name: str, plaza):
        """
        Create a plaza.
        
        Args:
            plaza_name: Name of the plaza
            plaza: plaza to create
            
        Returns:
            bool: True if created successfully
        """
        if plaza_name in self.plazas:
            print(f"plaza {plaza_name} already exists")
            return False
        
        self.plazas[plaza_name] = plaza
        self.owned_plazas[plaza_name] = plaza
        
        # Set the agent reference in the plaza
        if hasattr(plaza, 'agent'):
            plaza.agent = self
        
        # Start the plaza
        if hasattr(plaza, 'start'):
            plaza.start()
        
        print(f"Created plaza {plaza_name}")
        return True

    def remove_plaza(self, plaza_name: str):
        """
        Remove an owned plaza.
        
        Args:
            plaza_name: Name of the plaza
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        if plaza_name not in self.owned_plazas:
            print(f"plaza {plaza_name} is not owned by this agent")
            return False
        
        # Stop the plaza if it's running
        plaza = self.owned_plazas[plaza_name]
        if hasattr(plaza, "stop"):
            plaza.stop()
        
        # Remove from both owned and all plazas
        del self.owned_plazas[plaza_name]
        if plaza_name in self.plazas:
            del self.plazas[plaza_name]
            
        print(f"Removed plaza {plaza_name}")
        return True

    def connect_to_plaza(self, plaza_name: str, plaza):
        """
        Connect to a plaza.
        
        Args:
            plaza_name: Name of the plaza
            plaza: plaza object
            
        Returns:
            bool: True if connected successfully, False otherwise
        """
        if plaza_name in self.connected_plazas:
            print(f"Already connected to plaza {plaza_name}")
            return False
        
        # Set the agent reference in the plaza if it supports it
        if hasattr(plaza, 'agent') and plaza.agent is None:
            plaza.agent = self
        
        # Connect to the plaza
        self.connected_plazas[plaza_name] = plaza
        
        # Advertise on the plaza
        try:
            self.Advertise(plaza_name)
        except Exception as e:
            print(f"Error advertising on plaza {plaza_name}: {str(e)}")
            traceback.print_exc()
        
        print(f"Connected to plaza {plaza_name}")
        return True

    def disconnect_from_plaza(self, plaza_name: str):
        """
        Disconnect from a plaza.
        
        Args:
            plaza_name: Name of the plaza
            
        Returns:
            bool: True if disconnected successfully, False otherwise
        """
        # Cannot disconnect from owned plazas this way
        if plaza_name in self.owned_plazas:
            print(f"Cannot disconnect from owned plaza {plaza_name}. Use remove_plaza instead.")
            return False
            
        if plaza_name not in self.connected_plazas:
            print(f"Not connected to plaza {plaza_name}")
            return False
        
        # Stop advertisement thread if running
        if plaza_name in self.advertisement_threads:
            self.stop_advertisement_refresh(plaza_name)
        
        # Remove from both connected and all plazas
        del self.connected_plazas[plaza_name]
        if plaza_name in self.plazas:
            del self.plazas[plaza_name]
            
        print(f"Disconnected from plaza {plaza_name}")
        return True

    def get_plaza(self, plaza_name: str):
        """
        Get a plaza by name.
        
        Args:
            plaza_name: Name of the plaza
            
        Returns:
            object: The plaza, or None if not found
        """
        return self.plazas.get(plaza_name)

    def is_plaza_owner(self, plaza_name: str):
        """
        Check if the agent owns a plaza.
        
        Args:
            plaza_name: Name of the plaza
            
        Returns:
            bool: True if the agent owns the plaza, False otherwise
        """
        return plaza_name in self.owned_plazas

    def Advertise(self, plaza_name):
        """
        Advertise the agent on a plaza.
        
        Args:
            plaza_name: Name of the plaza
            
        Returns:
            bool: True if advertised successfully, False otherwise
        """
        try:
            # Check if the plaza is connected
            if plaza_name not in self.plazas:
                print(f"Plaza {plaza_name} not found")
                return False
            
            plaza = self.plazas[plaza_name]
            
            # Check if the plaza supports the Advertise practice
            if not hasattr(plaza, 'Advertise'):
                print(f"Plaza {plaza_name} does not support advertising")
                return False
            
            # Get the agent info
            agent_info = self.ToJson()
            #print(f"agent_info: {agent_info['components']['plugs']}")
            #print(f"agent.advertise agent_info: {agent_info}")
            # Advertise the agent on the plaza
            result = plaza.Advertise(self.agent_id, self.name, self.description, agent_info)
            
            print(f"Advertised agent {self.agent_id} on plaza {plaza_name}")

            # load peer list from plaza
            active_agents = plaza.UsePractice('ListActiveAgents')
            for agent in active_agents:
                # both agent_id and agent_name are used to identify the agent
                # agent_id is unique, agent_name is not
                self.peer_list[agent['agent_id']+ '@' + plaza_name] = agent
                self.peer_list[agent['agent_name']+ '@' + plaza_name] = agent
            return result
        except Exception as e:
            print(f"Error advertising agent: {str(e)}")
            traceback.print_exc()
            return False

    def start_advertisement_refresh(self, plaza_name: str, interval: int = 60):
        """
        Start refreshing advertisements on a plaza.
        
        Args:
            plaza_name: Name of the plaza
            interval: Refresh interval in seconds
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            if plaza_name not in self.plazas:
                print(f"Not connected to plaza {plaza_name}")
                return False
            
            # Check if already running
            if plaza_name in self.advertisement_threads:
                print(f"Advertisement refresh already running for plaza {plaza_name}")
                return False
            
            # Create a stop event
            stop_event = threading.Event()
            
            # Create and start the thread
            thread = threading.Thread(
                target=self._refresh_advertisements,
                args=(plaza_name, interval, stop_event)
            )
            thread.daemon = True
            thread.start()
            
            # Store thread info
            self.advertisement_threads[plaza_name] = {
                "thread": thread,
                "stop_event": stop_event,
                "interval": interval
            }
            
            print(f"Started advertisement refresh for plaza {plaza_name} (interval: {interval} seconds)")
            return True
        except Exception as e:
            print(f"Error starting advertisement refresh: {str(e)}")
            traceback.print_exc()
            return False

    def stop_advertisement_refresh(self, plaza_name: str):
        """
        Stop refreshing advertisements on a plaza.
        
        Args:
            plaza_name: Name of the plaza
            
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        try:
            # Check if running
            if plaza_name not in self.advertisement_threads:
                print(f"Advertisement refresh not running for plaza {plaza_name}")
                return False
            
            # Get thread info
            thread_info = self.advertisement_threads[plaza_name]
            
            # Signal the thread to stop
            thread_info["stop_event"].set()
            
            # Remove from the dictionary
            del self.advertisement_threads[plaza_name]
            
            print(f"Stopped advertisement refresh for plaza {plaza_name}")
            return True
        except Exception as e:
            print(f"Error stopping advertisement refresh: {str(e)}")
            traceback.print_exc()
            return False

    def _refresh_advertisements(self, plaza_name: str, interval: int, stop_event: threading.Event):
        """
        Refresh advertisements on a plaza periodically.
        
        Args:
            plaza_name: Name of the plaza
            interval: Refresh interval in seconds
            stop_event: Event to signal when to stop
        """
        try:
            while not stop_event.is_set():
                try:
                    # Refresh advertisement
                    self.Advertise(plaza_name)
                except Exception as e:
                    print(f"Error refreshing advertisement on plaza {plaza_name}: {str(e)}")
                    traceback.print_exc()
                
                # Wait for the next refresh or until stopped
                stop_event.wait(interval)
        except Exception as e:
            print(f"Error in advertisement refresh thread: {str(e)}")
            traceback.print_exc()

    def search_advertisements(self, plaza_name: str, query: Dict[str, Any] = None):
        """
        Search for advertisements on a plaza.
        
        Args:
            plaza_name: Name of the plaza
            query: Search criteria
            
        Returns:
            List[Dict]: List of advertisements matching the criteria
        """
        try:
            if plaza_name not in self.plazas:
                print(f"Not connected to plaza {plaza_name}")
                return []
            
            plaza = self.plazas[plaza_name]
            
            # Check if the plaza has the search_advertisements practice
            if hasattr(plaza, "search_advertisements"):
                # Search for advertisements
                advertisements = plaza.search_advertisements(query)
                return advertisements
            else:
                print(f"Plaza {plaza_name} does not support search_advertisements practice")
                return []
        except Exception as e:
            print(f"Error searching advertisements on plaza {plaza_name}: {str(e)}")
            traceback.print_exc()
            return []

    def request(self, plaza_name: str, target_agent_id: str, practice: str, **kwargs):
        """
        Send a request to another agent.
        
        Args:
            plaza_name: Name of the plaza
            target_agent_id: ID of the target agent
            practice: practice to request
            **kwargs: Arguments for the practice
            
        Returns:
            dict: Response from the target agent
        """
        if plaza_name not in self.plazas:
            print(f"Not connected to plaza {plaza_name}")
            return {"status": "error", "message": f"Not connected to plaza {plaza_name}"}
        
        plaza = self.plazas[plaza_name]
        
        try:
            response = plaza.request(target_agent_id, practice, **kwargs)
            return response
        except Exception as e:
            print(f"Error sending request to agent {target_agent_id} on plaza {plaza_name}: {str(e)}")
            traceback.print_exc()
            return {"status": "error", "message": str(e)}

    def start(self, auto_refresh=False):
        """
        Start the agent.
        
        Args:
            auto_refresh: Whether to automatically start refreshing advertisements
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.running:
            print(f"Agent {self.name} is already running")
            return False
        
        self.running = True
        
        # Start all plugs
        for plug_name, plug in self.plugs.items():
            if hasattr(plug, 'start'):
                try:
                    plug.start()
                except Exception as e:
                    print(f"Error starting plug {plug_name}: {str(e)}")
                    traceback.print_exc()
        
        # Start all plazas
        for plaza_name, plaza in self.owned_plazas.items():
            if hasattr(plaza, 'start'):
                try:
                    plaza.start()
                except Exception as e:
                    print(f"Error starting plaza {plaza_name}: {str(e)}")
                    traceback.print_exc()
        
        # Advertise on all plazas
        for plaza_name, plaza in self.plazas.items():
            try:
                self.Advertise(plaza_name)
            except Exception as e:
                print(f"Error advertising on plaza {plaza_name}: {str(e)}")
                traceback.print_exc()
        
        # Start automatic advertisement refresh if requested
        # Note: create-agent.py will call RefreshPractice based on command-line arguments,
        # so this is only needed if starting the agent in another way
        if auto_refresh:
            try:
                # Use RefreshPractice with duration=0 (indefinite) and interval=10 seconds
                self.RefreshPractice(duration=0, interval=10)
                print(f"Started automatic advertisement refresh for agent {self.name}")
            except Exception as e:
                print(f"Error starting advertisement refresh: {str(e)}")
                traceback.print_exc()
        
        print(f"Agent {self.name} started")
        return True

    def stop(self):
        """
        Stop the agent and all its components.
        """
        #print(f"Stopping agent {self.name}, running: {self.running}")
        if not self.running:
            print(f"Agent {self.name} is not running")
            return
        
        # Stop the refresh thread if it exists
        print(f"Stopping refresh thread for agent {self.name}")
        if self.refresh_stop_event:
            self.refresh_stop_event.set()
            if self.refresh_thread and self.refresh_thread.is_alive():
                self.refresh_thread.join(timeout=2)
            self.refresh_thread = None
            self.refresh_stop_event = None
        
        # Update stop time for all plazas
        print(f"Updating agent stop time for all plazas: {list(self.plazas.keys())}")
        for plaza_name in list(self.plazas.keys()):
            print(f"Updating agent stop time for plaza {plaza_name}")
            try:
                self.update_agent_stop_time(plaza_name)
            except Exception as e:
                print(f"Error updating agent stop time for plaza {plaza_name}: {str(e)}")
                traceback.print_exc()
        
        # Stop all advertisement refresh threads
        for plaza_name in list(self.advertisement_threads.keys()):
            print(f"Stopping advertisement refresh for plaza {plaza_name}")
            self.stop_advertisement_refresh(plaza_name)
        
        # Stop all pits
        for pit_type, pit_type_dict in list(self.pits.items()):
            for pit_name, pit in pit_type_dict.items():
                try:
                    if hasattr(pit, 'stop') and callable(pit.stop):
                        pit.stop()  
                except Exception as e:
                    print(f"Error stopping pit {pit_name}: {str(e)}")
                    traceback.print_exc()
            
        # Disconnect from all plazas
        for plaza_name in list(self.connected_plazas.keys()):
            try:
                self.disconnect_from_plaza(plaza_name)
            except Exception as e:
                print(f"Error disconnecting from plaza {plaza_name}: {str(e)}")
                traceback.print_exc()
        
        # Remove all plazas
        for plaza_name in list(self.owned_plazas.keys()):
            try:
                self.remove_plaza(plaza_name)
            except Exception as e:
                print(f"Error removing plaza {plaza_name}: {str(e)}")
                traceback.print_exc()
        
        self.running = False
        print(f"Agent {self.name} (ID: {self.agent_id}) stopped")

    def action(self):
        """
        Perform agent actions.
        
        This method is called in a loop to allow the agent to perform actions.
        It processes messages from plugs, handles requests, and performs other tasks.
        
        Returns:
            bool: True if actions were performed, False otherwise
        """
        if not self.running:
            print(f"Agent {self.name} is not running")
            return False
            
        # Process messages from plugs
        for pit_name, pit in self.plugs.items():
            if hasattr(pit, "receive") and callable(pit.receive):
                message = pit.receive()
                if message:
                    print(f"Received message on pit {pit_name}: {message}")
                    # Process the message based on its type
                    if isinstance(message, dict):
                        if "request" in message:
                            # Handle practice request
                            request = message["request"]
                            practice = request.get("practice")
                            if practice:
                                self.handle_practice_request(pit_name, message)
        
        # Check for expired advertisements
        for plaza_name, plaza in self.plazas.items():
            if hasattr(plaza, "clean_expired_advertisements"):
                plaza.clean_expired_advertisements()
                
        # Update environment information periodically
        if time.time() % 60 < 1:  # Update roughly every minute
            self.environments = self.detect_environments()
            
        return True
        
    def handle_practice_request(self, message:UsePracticeRequest):
        """
        Handle a practice request.
        
        Args:
            message: Message containing the request
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        request = message["request"]
        practice = request.get("practice")
        args = request.get("args", {})
        sender_id = request.get("sender_id")
        request_id = request.get("request_id")
        plaza_name = request.get("plaza_name")
        
        # Add or update peer information
        if sender_id and plaza_name:
            peer_address = str(AgentAddress(sender_id, plaza_name))
            current_time = datetime.now()
            
            if peer_address not in self.peer_list:
                self.peer_list[peer_address] = {
                    "agent_id": sender_id,
                    "plaza_name": plaza_name,
                    "first_seen": current_time,
                    "last_seen": current_time,
                    "practices": set(),
                    "connection_count": 1,
                    "pit_name": pit_name
                }
                if not args.debug:
                    log(f"New peer connected: {peer_address} through {pit_name}")
            else:
                self.peer_list[peer_address].update({
                    "last_seen": current_time,
                    "connection_count": self.peer_list[peer_address]["connection_count"] + 1,
                    "pit_name": pit_name
                })
                if not args.debug:
                    log(f"Existing peer reconnected: {peer_address} through {pit_name}")
            
            # Add the practice to peer's known practices
            if practice:
                self.peer_list[peer_address]["practices"].add(practice)
        
        print(f"Handling practice request: {practice} from {sender_id}")
        
        # Find the pit with the practice
        for pit_type, pit_type_dict in self.pits.items():
            for pit_name, pit in pit_type_dict.items():
                if hasattr(pit, "HasPractice") and pit.HasPractice(practice):
                    # Execute the practice
                    try:
                        result = pit.UsePractice(practice, **args)
                        
                        # Send response is UsePracticeResponse
                        
                        response = UsePracticeResponse(result, request_id)
                        
                        # Get the pit that received the request
                        source_pit = self.get(pit_name)
                        if source_pit and hasattr(source_pit, "send"):
                            source_pit.send(response)
                            
                        return True
                    except Exception as e:
                        # Send error response
                        traceback.print_exc()
                        response = {
                            "response": {
                                "status": "error",
                                "error": str(e),
                                "request_id": request_id
                            },
                            "sender_id": self.agent_id,
                            "receiver_id": sender_id
                        }
                        
                        # Get the pit that received the request
                        for pit_type, pit_type_dict in self.pits.items():
                            for pit_name, pit in pit_type_dict.items():
                                if pit_name == pit_name:
                                    source_pit = pit
                                    break
                        if source_pit and hasattr(source_pit, "send"):
                            source_pit.send(response)
                            
                        return False
        
        # practice not found
        response = {
            "response": {
                "status": "error",
                "error": f"practice {practice} not found",
                "request_id": request_id
            },
            "sender_id": self.agent_id,
            "receiver_id": sender_id
        }
        
        # Get the pit that received the request
        source_pit = self.pits.get(pit_name)
        if source_pit and hasattr(source_pit, "send"):
            source_pit.send(response)
            
        return False

    def add_plaza(self, plaza_type: str, name: str, description: str = None, **kwargs):
        """
        Add a plaza to the agent.
        
        Args:
            plaza_type: Type of plaza to add
            name: Name of the plaza
            description: Description of the plaza
            **kwargs: Additional arguments to pass to the plaza constructor
        
        Returns:
            The created plaza
        """
        try:
            # Import the plaza class dynamically
            if '.' in plaza_type:
                module_name, class_name = plaza_type.rsplit('.', 1)
            else:
                # Default to prompits.plazas package
                module_name = f"prompits.plazas.{plaza_type}"
                class_name = plaza_type
            
            # Try to import the module
            try:
                module = importlib.import_module(module_name)
            except ImportError:
                # If not found in prompits.plazas, try direct import
                module = importlib.import_module(plaza_type)
                class_name = plaza_type.split('.')[-1]
            
            # Get the class
            plaza_class = getattr(module, class_name)
            
            # Create an instance of the plaza
            plaza = plaza_class(name=name, description=description, agent=self, **kwargs)
            
            # Add the plaza to the agent
            self.plazas[name] = plaza
            
            # Add the plaza's practices to the agent
            for practice_name, practice_func in plaza.practices.items():
                self.AddPractice(Practice(f"{name}/{practice_name}", practice_func) )
                print(f"Added plaza practice {name}/{practice_name} to agent {self.name}")
            
            # Start the plaza
            if hasattr(plaza, 'start'):
                plaza.start()
            
            return plaza
        except Exception as e:
            print(f"Error adding plaza: {str(e)}")
            traceback.print_exc()
            return None

    def set_message_handler(self, handler):
        """
        Set a message handler function for the agent.
        
        The handler function should accept two arguments:
        - message: The received message
        - agent: The agent instance
        
        Args:
            handler: The handler function
            
        Returns:
            bool: True if set successfully
        """
        self.message_handler = handler
        
        # Set the handler for all plugs
        for plug_name, plug in self.plugs.items():
            if hasattr(plug, "set_message_handler"):
                plug.set_message_handler(lambda message: handler(message, self))
        
        return True

    def ConnectAgent(self, agent_address: AgentAddress, plug_name: str=None):
        """
        Connect to an agent.
        """
        # check if the agent is already connected
        if agent_address in self.connected_agents:
            print(f"Already connected to agent {agent_address}")
            return
        
        # connect to the agent
        # get agent's info from the agent address
        agent_info = self.get_agent_info(agent_address)
        if not agent_info:
            print(f"Failed to get agent info for {agent_address}")
            return
        
        # connect to the agent
        # check all plugs of the agent
        # for all plugs of the agent, check if the plug is connectable
        if plug_name:
            if plug_name not in agent_info.get("plugs", {}).keys():
                print(f"Plug {plug_name} not found in agent {agent_address}")
                return
            plug = agent_info.get("plugs", {}).get(plug_name)
            if not plug.get("connectable"):
                print(f"Plug {plug_name} is not connectable")
                return
            


    def get_agent_info(self, agent_address: AgentAddress):
        """
        Get agent info from the agent address.
        """
        # get agent's info from plaza
        plaza = self.plazas[agent_address.plaza_name]
        if not plaza:
            print(f"Not connected to plaza {agent_address.plaza_name}")
            return None
        
        return plaza.UsePractice("GetAgentInfo", agent_address)

    def update_agent_stop_time(self, plaza_name: str):
        """
        Update the stop_time field in the agents table when the agent stops.
        
        Args:
            plaza_name: Name of the plaza with a DatabasePool
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        if plaza_name not in self.plazas:
            print(f"Not connected to plaza {plaza_name}")
            return False
        
        plaza = self.plazas[plaza_name]
        
        # Find a DatabasePool in the plaza
        if not hasattr(plaza, 'pools'):
            print(f"plaza {plaza_name} has no pools")
            return False
        
        db_pool = None
        for pool in plaza.pools:
            if hasattr(pool, '__class__') and issubclass(pool.__class__, DatabasePool):
                db_pool = pool
                break
        
        if not db_pool:
            print(f"No DatabasePool found in plaza {plaza_name}")
            return False
        
        # Current time
        current_time = datetime.now()
        
        try:
            # Don't have to Make sure we have a fresh connection
            # just make sure the connection is open
            if not db_pool._IsConnected():
                db_pool._Connect()
            
            # Check if the agent exists
            existing_agents = db_pool.UsePractice("GetTableData", 'agents', {"agent_id": self.agent_id})
            
            if existing_agents:
                # Update existing agent
                db_pool.UsePractice("Update",
                    table_name='agents',
                    data={
                        "stop_time": current_time,
                        "status": "inactive"
                    },
                    where_clause={"agent_id": self.agent_id}
                )
                print(f"Updated agent stop time for {self.name} on plaza {plaza_name}")
                if hasattr(db_pool, 'Commit'):
                    db_pool.Commit()
                
                return True
            else:
                print(f"Agent {self.name} not found in 'agents' table")
                return False
        except Exception as e:
            if hasattr(db_pool, 'Rollback'):
                db_pool.Rollback()
            print(f"Error updating agent stop time: {str(e)}")
            traceback.print_exc()
            return False


    # override list_practices from Pit
    def ListPractices(self,name_only=False):
        """
        List all practices of the agent.
        
        Returns:
            list: List of practice names
        """
        # return list of practices from pits
        # and add the agent's practices to the list
        # key as pitname/practicename
        
        # print all pits name
        #print(f"Pits: {self.pits.keys()}")
        #print(f"Agent practices: {self.practices.keys()}")
        practice_list = []
        if name_only:
            practice_list.extend([f"{practice}" for practice in self.practices.keys()])
        else:
            practice_list.extend([{f"{practice}":self.practices[practice].ToJson()} for practice in self.practices.keys()])
        for pit_type, pit_type_dict in self.pits.items():
            for pit_name, pit in pit_type_dict.items():
                if name_only:
                    practice_list.extend([f"{pit_name}/{practice}" for practice in pit.practices.keys()])
                else:
                    practice_list.extend([{f"{pit_name}/{practice}":pit.practices[practice].ToJson()} for practice in pit.practices.keys()])
        return practice_list
    
    def UsePracticeRemote(self, practice: str, remote_agent_address: AgentAddress, *args, **kwargs):
        """
        Use a practice of a remote agent.
        """
        # if agent_address is a string, convert it to an AgentAddress
        if isinstance(remote_agent_address, str):
            remote_agent_address = AgentAddress(remote_agent_address.split("@")[0], remote_agent_address.split("@")[1])
        request=UsePracticeRequest(practice, AgentAddress(self.agent_id, self.plazas[remote_agent_address.plaza_name].name), remote_agent_address, *args, **kwargs)
        print(f"\n\n*** UsePracticeRemote: Sending message to {remote_agent_address}")
        print(f"UsePracticeRemote: SendMessage: {request}")
        self.SendMessage(request, [remote_agent_address])
        print(f"UsePracticeRemote: Receiving message from {remote_agent_address}")
        # wait for 5 second or until a response is received 
        start_time = time.time()
        while time.time() - start_time < 5:
            response_list = self.ReceiveMessage()
            if response_list:
                break
        if not response_list:
            raise ValueError(f"No response received from {remote_agent_address}")

        print(f"UsePracticeRemote:")
        for response in response_list:
            print(f"UsePracticeRemote: response: {response}")
        if response_list[0].body['status'] == 'success':
            return response_list[0].body['result']
        else:
            raise ValueError(f"Failed to use practice {practice} of agent {remote_agent_address}")
    
    def UsePractice(self, practice, *args, **kwargs):
        """
        Use a practice of the agent.
        
        Args:
            practice: Name of the practice
            *args: Positional arguments for the practice
            **kwargs: Keyword arguments for the practice
            
        Returns:
            Any: Result of the practice
        """
        # check if practice is a string with pitname/practicename
        if "/" in practice:
            pit_use, practice_name = practice.split("/")
            for pit_type, pit_type_dict in self.pits.items():
                for pit_name, pit in pit_type_dict.items():
                    if pit_name == pit_use:
                        return pit.UsePractice(practice_name, *args, **kwargs)
            else:
                raise ValueError(f"practice {practice} not found in agent or any pit")
        else:
            if practice in self.practices:
                return self.practices[practice].function(*args, **kwargs)
            else:
                raise ValueError(f"practice {practice} not found in agent")
            
            
            raise ValueError(f"practice {practice} not found in agent or any pit")
            
    def StopAgent(self):
        """
        Stop the agent.
        
        Returns:
            str: Status message
        """
        try:
            # Stop all advertisement refresh threads
            for plaza_name in list(self.advertisement_threads.keys()):
                print(f"Stopping advertisement refresh for plaza {plaza_name}")
                self.stop_advertisement_refresh(plaza_name)
            
            # Stop the main refresh thread if running
            if self.refresh_thread and self.refresh_stop_event:
                self.refresh_stop_event.set()
                self.refresh_thread.join(timeout=1)
                self.refresh_thread = None
                self.refresh_stop_event = None
            
            # Update stop time on all plazas
            for plaza_name, plaza in self.plazas.items():
                if hasattr(plaza, "update_agent_stop_time"):
                    plaza.update_agent_stop_time(self.agent_id)
            
            # Stop all plazas
            for plaza_name, plaza in self.plazas.items():
                if hasattr(plaza, "stop"):
                    plaza.stop()
            
            # Stop all plugs
            for plug_name, plug in self.plugs.items():
                if hasattr(plug, "stop"):
                    plug.stop()
            
            # Stop all pits
            for pit_type, pit_type_dict in self.pits.items():
                for pit_name, pit in pit_type_dict.items():
                    if hasattr(pit, "stop"):
                        pit.stop()
            
            self.running = False
            
            return f"Agent {self.name} stopped"
        except Exception as e:
            print(f"Error stopping agent: {str(e)}")
            traceback.print_exc()
            return f"Error stopping agent: {str(e)}"
        
    def RefreshPractice(self, duration: int = 0, interval: int = 60):
        """
        Refresh agent advertisements on all connected plazas.
        
        Args:
            duration: Duration in seconds to refresh advertisements (0 for indefinite)
            interval: Refresh interval in seconds
            
        Returns:
            str: Status message
        """
        try:
            # Find all plazas to advertise on
            plazas = list(self.plazas.keys())
            if not plazas:
                return f"Agent {self.name} has no plazas to advertise on"
            
            # Stop any existing refresh threads
            for plaza_name in list(self.advertisement_threads.keys()):
                self.stop_advertisement_refresh(plaza_name)
            
            # Create a stop event for the refresh thread
            self.refresh_stop_event = threading.Event()
            
            # Create and start the refresh thread
            self.refresh_thread = threading.Thread(
                target=self._refresh_all_advertisements,
                args=(plazas, interval, duration, self.refresh_stop_event)
            )
            self.refresh_thread.daemon = True
            self.refresh_thread.start()
            
            return f"Started advertisement refresh for {'indefinite time' if duration <= 0 else duration} seconds with {interval} second intervals on plazas: {plazas}"
        except Exception as e:
            print(f"Error starting advertisement refresh: {str(e)}")
            traceback.print_exc()
            return f"Error starting advertisement refresh: {str(e)}"

    def _refresh_all_advertisements(self, plazas: List[str], interval: int, duration: int, stop_event: threading.Event):
        """
        Refresh advertisements on all plazas periodically.
        
        Args:
            plazas: List of plaza names
            interval: Refresh interval in seconds
            duration: Duration in seconds (0 for indefinite)
            stop_event: Event to signal when to stop
        """
        try:
            start_time = time.time()
            
            while not stop_event.is_set():
                # Check if duration has elapsed
                if duration > 0 and time.time() - start_time > duration:
                    break
                
                # Refresh advertisements on all plazas
                for plaza_name in plazas:
                    try:
                        self.Advertise(plaza_name)
                    except Exception as e:
                        print(f"Error refreshing advertisement on plaza {plaza_name}: {str(e)}")
                        traceback.print_exc()
                
                # Wait for the next refresh or until stopped
                stop_event.wait(interval)
        except Exception as e:
            print(f"Error in refresh all advertisements thread: {str(e)}")
            traceback.print_exc()

    def AddPractice(self, practice, func=None):
        """
        Add a practice to the agent.
        
        Args:
            practice: Practice object or name of the practice
            func: Function to call when the practice is used (if practice is a name)
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if func is not None:
            # If a function is provided, create a Practice object
            from prompits.Practice import Practice
            self.practices[practice] = Practice(practice, func)
        else:
            # If a Practice object is provided, add it directly
            self.practices[practice.name] = practice
        return True

    def add_plug(self, plug):
        """
        Add a plug to the agent.
        
        Args:
            plug: Plug to add
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        self.plugs[plug.name] = plug
        
        # Set the agent reference in the plug if it has a set_agent method
        if hasattr(plug, 'set_agent') and callable(plug.set_agent):
            plug.set_agent(self)
            
        # Add the plug's practices to the agent
        for practice_name, practice_func in plug.practices.items():
            self.AddPractice(f"{plug.name}/{practice_name}", practice_func)
            print(f"Added pool practice {plug.name}/{practice_name} to agent {self.name}")
            
        return True

