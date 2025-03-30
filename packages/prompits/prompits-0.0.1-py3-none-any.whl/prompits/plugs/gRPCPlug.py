# gRPCPlug is a plug that uses gRPC to communicate with other agents
# gRPC is a high-performance, open-source and general RPC framework that puts mobile and HTTP/2 first

from datetime import datetime
import json
import traceback
import threading
import time
import uuid
import grpc
from concurrent import futures
from typing import Dict, Any, Optional, List, Union, Callable

from prompits.AgentAddress import AgentAddress
from prompits.Practice import Practice
from prompits.Plug import Plug
from prompits.Message import Message, Attachment

# Import the generated gRPC code
# Note: You'll need to generate these files from your .proto definitions
try:
    from prompits.plugs.protos import agent_pb2
    from prompits.plugs.protos import agent_pb2_grpc
except ImportError:
    # Placeholder for when protos aren't generated yet
    class agent_pb2:
        class Message:
            def __init__(self):
                self.id = ""
                self.type = ""
                self.content = ""
                self.timestamp = 0
                
        class AgentInfo:
            def __init__(self):
                self.agent_id = ""
                self.agent_name = ""
                
    class agent_pb2_grpc:
        class AgentServicer:
            pass
            
        class AgentStub:
            pass
            
        def add_AgentServicer_to_server(servicer, server):
            pass

# Define the gRPC service
class AgentServicer(agent_pb2_grpc.AgentServicer):
    def __init__(self, grpc_plug):
        self.grpc_plug = grpc_plug
        
    def SendMessage(self, request, context):
        # Convert protobuf message to dict
        message = {
            'id': request.id,
            'type': request.type,
            'content': request.content,
            'timestamp': request.timestamp
        }
        
        # Trigger message event
        self.grpc_plug.trigger_event('message', message=message)
        
        # Add to message queue
        with self.grpc_plug.message_lock:
            self.grpc_plug.message_queue.append(message)
        
        # Return response
        return agent_pb2.MessageResponse(success=True, message="Message received")
    
    def Echo(self, request, context):
        # Echo the message back
        return agent_pb2.Message(
            id=request.id,
            type="echo_response",
            content=request.content,
            timestamp=int(time.time())
        )
        
    def GetAgentInfo(self, request, context):
        # Get agent information from the plug's agent
        agent = self.grpc_plug.agent if hasattr(self.grpc_plug, 'agent') else None
        
        if not agent:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("Agent information not available")
            return agent_pb2.AgentInfo()
            
        # Get capabilities (practices)
        capabilities = []
        if hasattr(agent, 'practices'):
            capabilities.extend(agent.practices.keys())
            
        # Create and return agent info
        return agent_pb2.AgentInfo(
            agent_id=getattr(agent, 'agent_id', str(uuid.uuid4())),
            agent_name=getattr(agent, 'name', "Unknown"),
            description=getattr(agent, 'description', ""),
            capabilities=capabilities
        )
    
    
    
    def ListPractices(self, request, context):
        # Get agent
        agent = self.grpc_plug.agent if hasattr(self.grpc_plug, 'agent') else None
        
        if not agent:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("Agent not available")
            return agent_pb2.PracticeList()
            
        # Get practices
        practice_list = []
        
        # Add agent practices
        if hasattr(agent, 'practices'):
            for name, practice in agent.practices.items():
                # Get practice info
                practice_info = agent_pb2.Practice(
                    name=name,
                    description=practice.__doc__ if hasattr(practice, '__doc__') and practice.__doc__ else ""
                )
                
                # Add parameters if available
                if hasattr(practice, '__code__'):
                    for i, param_name in enumerate(practice.__code__.co_varnames[:practice.__code__.co_argcount]):
                        if param_name == 'self':
                            continue
                            
                        # Create parameter
                        param = agent_pb2.Parameter(
                            name=param_name,
                            type="unknown",
                            required=i >= (practice.__code__.co_argcount - len(practice.__defaults__ or []))
                        )
                        
                        # Add default value if available
                        if not param.required and practice.__defaults__:
                            default_idx = i - (practice.__code__.co_argcount - len(practice.__defaults__))
                            if default_idx >= 0:
                                param.default_value = str(practice.__defaults__[default_idx])
                                
                        # Add parameter to practice
                        practice_info.parameters.append(param)
                        
                # Add practice to list
                practice_list.append(practice_info)
                
        # Return practice list
        return agent_pb2.PracticeList(practices=practice_list)
        
    def ExecutePractice(self, request, context):
        # Get agent
        agent = self.grpc_plug.agent if hasattr(self.grpc_plug, 'agent') else None
        
        if not agent:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("Agent not available")
            return agent_pb2.PracticeResponse(success=False, error="Agent not available")
            
        # Get practice name
        practice_name = request.practice_name
        
        # Check if practice exists
        if not hasattr(agent, 'UsePractice'):
            return agent_pb2.PracticeResponse(
                success=False,
                error="Agent does not support UsePractice method"
            )
            
        # Convert parameters
        params = {}
        for key, value in request.parameters.items():
            # Try to convert to appropriate type
            try:
                # Try as JSON first
                params[key] = json.loads(value)
            except json.JSONDecodeError:
                # Use as string
                params[key] = value
                
        # Execute practice
        try:
            result = agent.UsePractice(practice_name, **params)
            
            # Convert result to string if needed
            if not isinstance(result, str):
                try:
                    result = json.dumps(result)
                except:
                    result = str(result)
                    
            return agent_pb2.PracticeResponse(
                success=True,
                result=result
            )
        except Exception as e:
            return agent_pb2.PracticeResponse(
                success=False,
                error=str(e)
            )

class gRPCPlug(Plug):
    def __init__(self, name: str, description: str = None, host: str = "localhost", port: int = 9000, is_server: bool = False):
        super().__init__(name, description or f"gRPC Plug {name}")
        self.host = host
        self.port = port
        self.is_server = is_server
        self.server = None
        self.channel = None
        self.stub = None
        self.running = False
        self.connected = False
        self.message_queue = []
        self.message_lock = threading.Lock()
        self.event_handlers = {}
        
        if self.is_server:
            self._Listen({})

    def SendMessage(self, agent:AgentAddress, message: Message, plug_info:Dict[str, Any]):
        """Send a message via gRPC
        Args:
            agent: AgentAddress
            message: Message
            plug_info: 
                {
                    "host": str,
                    "port": int
                }
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.connected:
            # try to connect to the agent
            self._Connect(agent, plug_info)
            if not self.connected:
                print(f"gRPC Plug {self.name} is not connected")
                return False
        

        server_address = f"{plug_info['host']}:{plug_info['port']}"
        print(f"Sending message to {server_address}")

        # with grpc.insecure_channel(server_address) as channel:

        # get the stub for the agent
        stub = agent_pb2_grpc.AgentStub(self.channel)
        # print("Message Json:")
        # print(message)
        # print(json.dumps(message.ToJson()))
        # if message is Message object, convert it to a string
        timestamp = int(time.time())
        if isinstance(message, str):
            msg_str = message
        else:
            print(f"gRPCPlug.SendMessage(): Message: {message.ToJson()}")
            #message.sent_time = timestamp
            json_msg = message.ToJson()
            json_msg['sent_time'] = timestamp
            if isinstance(json_msg['sender'], AgentAddress):
                json_msg['sender'] = json_msg['sender'].ToJson()
            if isinstance(json_msg['recipients'], list):
                for recipient in json_msg['recipients']:
                    if isinstance(recipient, AgentAddress):
                        recipient = recipient.ToJson()
            if isinstance(json_msg['attachments'], list):
                for attachment in json_msg['attachments']:
                    if isinstance(attachment, Attachment):
                        attachment = attachment.ToJson()
            msg_str = json.dumps(json_msg)
        # Create a message
        msg = agent_pb2.Message(
            id=str(uuid.uuid4()),
            type=message.type,
            content=msg_str,
            timestamp=timestamp
        )

        stub.SendMessage(msg)
        return True
    
        # Add gRPC-specific practices
    def _Listen(self, plugs_info:Dict[str, Any]):
        """Listen for incoming connections
        
        Args:
            plugs_info: Dictionary with connection information
            
        Returns:
            bool: True if listening successfully, False otherwise
        """
        if not self.is_server:
            print(f"gRPC Plug {self.name} is not a server")
            return False
            
        try:
            # Create a server
            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            
            # Add the servicer to the server
            agent_pb2_grpc.add_AgentServicer_to_server(AgentServicer(self), self.server)
            
            # Add a secure port
            # if self.port is 0, try to find an open port, starting at 9000
            if self.port == 0:
                for port in range(9000, 9100):
                    try:
                        server_address = f"{self.host}:{port}"
                        self.server.add_insecure_port(server_address)
                        self.port = port
                        break
                    except Exception as e:
                        print(f"Error adding insecure port {port}: {str(e)}")
                        continue
            else:
                server_address = f"{self.host}:{self.port}"
                self.server.add_insecure_port(server_address)
            
            # Start the server
            self.server.start()
            print(f"gRPC server {self.name} listening on {server_address}")
            
            self.running = True
            return True
        except Exception as e:
            print(f"Error starting gRPC server {self.name}: {str(e)}")
            traceback.print_exc()
            return False
    # connect to remote agent
    def _Connect(self, agent:AgentAddress, plugs_info:Dict[str, Any]):
        """Connect to an agent via gRPC
        
        Args:
            agent: AgentAddress
            plugs_info: Dictionary with connection information
                {
                    "host": str,
                    "port": int
                }
                
        Returns:
            bool: True if connected successfully, False otherwise
        """
        try:
                # if self.port is 0, try to find an open port, starting at 9000
            if self.port == 0:
                for port in range(9000, 9100):
                    try:
                        self.channel = grpc.insecure_channel(f"{self.host}:{port}")
                        self.stub = agent_pb2_grpc.AgentStub(self.channel)
                        self.connected = True
                        self.port = port
                        break
                    except Exception as e:
                        print(f"Error connecting to port {port}: {str(e)}")
                        continue
            else:
                host = plugs_info.get('host', self.host)
                port = plugs_info.get('port', self.port)
                server_address = f"{host}:{port}"
            print(f"Connecting to {server_address} via gRPC Plug {self.name}")
            
            # Create a channel
            self.channel = grpc.insecure_channel(server_address)
            
            # Create a stub
            self.stub = agent_pb2_grpc.AgentStub(self.channel)
            
            # Set connected flag
            self.connected = True
            
            print(f"Connected to {server_address} via gRPC Plug {self.name}")
            return True
        except Exception as e:
            print(f"Error connecting to agent via gRPC Plug {self.name}: {str(e)}")
            traceback.print_exc()
            self.connected = False
            return False
    
    def Connect(self):
        """Connect to the gRPC server or start a server"""
        if self.is_server:
            return self._Listen({})
        else:
            # Client mode - will connect when needed
            return True
            
    def Disconnect(self):
        """Disconnect from the gRPC server or stop the server"""
        try:
            if self.is_server and self.server:
                self.server.stop(0)
                self.server = None
                self.running = False
                print(f"gRPC server {self.name} stopped")
                
            if self.channel:
                self.channel.close()
                self.channel = None
                self.stub = None
                
            self.connected = False
            print(f"gRPC Plug {self.name} disconnected")
            return True
        except Exception as e:
            print(f"Error disconnecting gRPC Plug {self.name}: {str(e)}")
            traceback.print_exc()
            return False

    def _Send(self, message: Dict[str, Any]):
        """Send a message via gRPC"""
        if not self.connected:
            print(f"gRPC Plug {self.name} is not connected")
            return False
            
        if self.is_server:
            print(f"gRPC Plug {self.name} is a server and cannot send messages directly")
            return False
            
        try:
            # Convert dict to protobuf message
            grpc_message = agent_pb2.Message(
                id=message.get('id', str(uuid.uuid4())),
                type=message.get('type', 'message'),
                content=json.dumps(message.get('content', {})),
                timestamp=message.get('timestamp', int(time.time()))
            )
            
            # Send the message
            response = self.stub.SendMessage(grpc_message)
            print(f"Sent message via gRPC Plug {self.name}: {response.message}")
            return True
        except Exception as e:
            print(f"Error sending message via gRPC Plug {self.name}: {str(e)}")
            traceback.print_exc()
            return False

    def _send(self, message: Dict[str, Any]):
        """Internal method to send a message (required by Plug abstract class)"""
        return self.send(message)


    def _IsConnected(self) -> bool:
        """Check if the gRPC plug is connected
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.connected and self.channel is not None

    def _SendMessage(self, message):
        """Send a message (can be a Message object or dict)"""
        if isinstance(message, Message):
            return self.send(message.ToJson())
        else:
            return self.send(message)

    def ReceiveMessage(self, msg_count: int = 0):
        """Receive a message from the queue
        Args:
            msg_count: int, number of messages to receive. 0 means max 1000 messages.
        Returns:
            list[Message]: list of messages
        """
        # receive a message from the queue
        # pop individual messages from the queue and convert content to Message object

        msg_list:[Message] = []
        with self.message_lock:
            if not self.message_queue:
                return None
            if msg_count == 0:
                msg_count=1000
            for i in range(msg_count):
                # check if there are more messages in the queue
                if len(self.message_queue) > 0:
                    msg = self.message_queue.pop(0)
                    print(f"Received message: {msg}")
                    msg_json = json.loads(msg['content'])
                    if "sent_time" in msg_json:
                        msg_json['sent_time'] = datetime.fromtimestamp(msg_json['sent_time'])
                    else:
                        msg_json['sent_time'] = datetime.now()
                    if "attachments" in msg_json and msg_json['attachments'] is not None:
                        attachments = [Attachment(attachment['name'], attachment['content']) for attachment in msg_json['attachments']]
                    else:
                        attachments = None
                    msg_list.append(Message(msg_json['type'], msg_json['body'], msg_json['sender'], 
                                        msg_json['recipients'], attachments, msg_json['msg_id'], msg_json['sent_time']))
                else:
                    break
        return msg_list
                
    def _Echo(self, message: str):
        """Echo a message back to the sender"""
        if not self.connected or self.is_server:
            print(f"gRPC Plug {self.name} cannot echo messages")
            return {"error": "Cannot echo messages"}
            
        try:
            # Create a message
            grpc_message = agent_pb2.Message(
                id=str(uuid.uuid4()),
                type="echo",
                content=message,
                timestamp=int(time.time())
            )
            
            # Send the echo request
            response = self.stub.Echo(grpc_message)
            
            # Return the response
            return {
                "id": response.id,
                "type": response.type,
                "content": response.content,
                "timestamp": response.timestamp
            }
        except Exception as e:
            print(f"Error echoing message via gRPC Plug {self.name}: {str(e)}")
            traceback.print_exc()
            return {"error": str(e)}

    def register_event_handler(self, event_type: str, handler_func: Callable):
        """Register an event handler for a specific event type"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
            
        self.event_handlers[event_type].append(handler_func)
        print(f"Registered event handler for {event_type} events in gRPC Plug {self.name}")
        return True

    def unregister_event_handler(self, event_type: str, handler_func: Optional[Callable] = None):
        """Unregister an event handler"""
        if event_type not in self.event_handlers:
            print(f"No handlers registered for {event_type} events in gRPC Plug {self.name}")
            return False
            
        if handler_func is None:
            # Unregister all handlers for this event type
            self.event_handlers[event_type] = []
            print(f"Unregistered all handlers for {event_type} events in gRPC Plug {self.name}")
            return True
            
        if handler_func in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler_func)
            print(f"Unregistered handler for {event_type} events in gRPC Plug {self.name}")
            return True
            
        print(f"Handler not found for {event_type} events in gRPC Plug {self.name}")
        return False

    def trigger_event(self, event_type: str, **event_data):
        """Trigger an event and call all registered handlers"""
        if event_type not in self.event_handlers or not self.event_handlers[event_type]:
            return False
            
        for handler in self.event_handlers[event_type]:
            try:
                print(f"Triggering event {event_type} with data: {event_data}")
                handler(self, **event_data)
            except Exception as e:
                print(f"Error in event handler for {event_type} event: {str(e)}")
                traceback.print_exc()
                
        return True

    def start(self):
        """Start the gRPC plug"""
        return self.Connect()

    def stop(self):
        """Stop the gRPC plug"""
        return self.Disconnect()

    def ToJson(self):
        """Convert the gRPC plug to a JSON object"""
        json_data = super().ToJson()
        json_data.update({
            "host": self.host,
            "port": self.port,
            "type": "gRPCPlug",
            "is_server": self.is_server
        })
        return json_data

    def FromJson(self, json_data):
        """Initialize the gRPC plug from a JSON object"""
        super().FromJson(json_data)
        self.host = json_data.get("host", self.host)
        self.port = json_data.get("port", self.port)
        self.is_server = json_data.get("is_server", self.is_server)
        return self
        
    def set_agent(self, agent):
        """Set the agent reference for this plug"""
        self.agent = agent
        return self

    def _Disconnect(self, agent:AgentAddress, plugs_info:Dict[str, Any]):
        """Disconnect from an agent via gRPC
        
        Args:
            agent: AgentAddress
            plugs_info: Dictionary with connection information
            
        Returns:
            bool: True if disconnected successfully, False otherwise
        """
        try:
            if self.channel:
                self.channel.close()
                self.channel = None
                self.stub = None
            
            # Set connected flag
            self.connected = False
            
            print(f"Disconnected from agent via gRPC Plug {self.name}")
            return True
        except Exception as e:
            print(f"Error disconnecting from agent via gRPC Plug {self.name}: {str(e)}")
            traceback.print_exc()
            return False


