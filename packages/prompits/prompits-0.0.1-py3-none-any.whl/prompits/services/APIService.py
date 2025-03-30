# APIService is a Pit
# APIService can be initialized with a list of endpoints or OpenAPI spec
# APIService is an abstract class
# Has practices: GetEndpoints, GetOpenAPISpec

from typing import List, Dict, Any, Optional
import requests
from ..Pit import Pit
from prompits.Practice import Practice

class Endpoint:
    def __init__(self, path: str, method: str, description: str = None, parameters: List[Dict] = None, responses: Dict = None):
        self.path = path
        self.method = method
        self.description = description
        self.parameters = parameters or []
        self.responses = responses or {}
        self.body = None
    
    def to_dict(self):
        """Convert endpoint to dictionary"""
        return {
            "path": self.path,
            "method": self.method,
            "description": self.description,
            "parameters": self.parameters,
            "responses": self.responses
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create endpoint from dictionary"""
        return cls(
            path=data.get("path"),
            method=data.get("method"),
            description=data.get("description"),
            parameters=data.get("parameters"),
            responses=data.get("responses")
        )

class OpenAPI:
    def __init__(self, info: Dict, paths: Dict, components: Dict = None):
        self.info = info
        self.paths = paths
        self.components = components or {}
    
    def to_dict(self):
        """Convert OpenAPI to dictionary"""
        return {
            "info": self.info,
            "paths": self.paths,
            "components": self.components
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create OpenAPI from dictionary"""
        return cls(
            info=data.get("info", {}),
            paths=data.get("paths", {}),
            components=data.get("components", {})
        )

class APIService(Pit):
    def __init__(self, name: str, description: str = None, endpoints: List[Endpoint]=None, openapi_spec: OpenAPI=None, base_url: str = None):
        super().__init__(name, description)
        self.endpoints = endpoints or []
        self.openapi_spec = openapi_spec
        self.base_url = base_url
        self.AddPractice(Practice("GetEndpoints", self.GetEndpoints))
        self.AddPractice(Practice("GetOpenAPISpec", self.GetOpenAPISpec))
        
    def Request(self, endpoint: Endpoint, body: Dict = None, headers: Dict = None, params: Dict = None):
        """
        Request an endpoint.
        """
        # implement using requests
        if not self.base_url:
            raise ValueError("Base URL is not set")
            
        url = f"{self.base_url}{endpoint.path}"
        request_body = body if body is not None else endpoint.body
        response = requests.request(endpoint.method, url, json=request_body, headers=headers, params=params)
        return response.json()
    
    def ToJson(self):
        """
        Convert the service to a JSON object.
        
        Returns:
            dict: JSON representation of the service
        """
        endpoints_json = []
        for endpoint in self.endpoints:
            endpoints_json.append(endpoint.to_dict())
        
        openapi_json = None
        if self.openapi_spec:
            openapi_json = self.openapi_spec.to_dict()
        json_data = super().ToJson()
        json_data.update({
            "base_url": self.base_url,
            "endpoints": endpoints_json,
            "openapi_spec": openapi_json
        })
        return json_data
    
    def FromJson(self, json_data):
        """
        Initialize the service from a JSON object.
        
        Args:
            json_data: JSON object containing service configuration
            
        Returns:
            APIService: The initialized service
        """
        self.name = json_data.get("name", self.name)
        self.description = json_data.get("description", self.description)
        self.base_url = json_data.get("base_url", self.base_url)
        
        # Load endpoints
        if "endpoints" in json_data:
            self.endpoints = []
            for endpoint_data in json_data["endpoints"]:
                self.endpoints.append(Endpoint.from_dict(endpoint_data))
        
        # Load OpenAPI spec
        if "openapi_spec" in json_data and json_data["openapi_spec"]:
            self.openapi_spec = OpenAPI.from_dict(json_data["openapi_spec"])
        
        return self
    
    def GetEndpoints(self):
        """
        Get the list of endpoints for this API service.
        
        Returns:
            List[Endpoint]: List of endpoints
        """
        return self.endpoints

    def GetOpenAPISpec(self):
        """
        Get the OpenAPI specification for this API service.
        
        Returns:
            OpenAPI: OpenAPI specification
        """
        return self.openapi_spec
    
    def AddEndpoint(self, endpoint: Endpoint):
        """
        Add an endpoint to this API service.
        
        Args:
            endpoint (Endpoint): The endpoint to add
            
        Returns:
            bool: True if added successfully
        """
        self.endpoints.append(endpoint)
        return True
    
    def RemoveEndpoint(self, path: str, method: str):
        """
        Remove an endpoint from this API service.
        
        Args:
            path (str): The path of the endpoint
            method (str): The HTTP method of the endpoint
            
        Returns:
            bool: True if removed successfully, False if not found
        """
        for i, endpoint in enumerate(self.endpoints):
            if endpoint.path == path and endpoint.method == method:
                self.endpoints.pop(i)
                return True
        return False
    
    def SetOpenAPISpec(self, openapi_spec: OpenAPI):
        """
        Set the OpenAPI specification for this API service.
        
        Args:
            openapi_spec (OpenAPI): The OpenAPI specification
            
        Returns:
            bool: True if set successfully
        """
        self.openapi_spec = openapi_spec
        return True
    
    def GenerateOpenAPISpec(self):
        """
        Generate an OpenAPI specification from the endpoints.
        
        Returns:
            OpenAPI: Generated OpenAPI specification
        """
        if not self.endpoints:
            return None
        
        paths = {}
        for endpoint in self.endpoints:
            if endpoint.path not in paths:
                paths[endpoint.path] = {}
            
            paths[endpoint.path][endpoint.method.lower()] = {
                "description": endpoint.description or "",
                "parameters": endpoint.parameters,
                "responses": endpoint.responses
            }
        
        info = {
            "title": self.name,
            "description": self.description or f"API Service: {self.name}",
            "version": "1.0.0"
        }
        
        self.openapi_spec = OpenAPI(info=info, paths=paths)
        return self.openapi_spec

