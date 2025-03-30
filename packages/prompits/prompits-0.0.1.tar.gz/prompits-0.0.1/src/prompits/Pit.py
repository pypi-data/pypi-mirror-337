# Pit is the basic element of a multi-agent system.
# It provides a way to store and retrieve information.
# An agent can contain multiple pits.
# A pit has a list of practices.
# practices are the actions that a pit can perform.
# practice associated with a function.
# Other pits can use the practices though a function UsePractice()
# Pit is an abstract class.
# Pit can be described as a JSON object ToJson()
# Pit can be initialized from a JSON object __init__(json)
# Sample JSON:
# {
#     "name": "Pit1",
#     "description": "Pit1 description"
# }

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
import inspect  
from prompits.Practice import Practice
class Pit(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.practices = {}
        
        # Add standard practices
        practice=Practice("ListPractices", self.ListPractices)
        print(f"practice: {practice}")
        self.AddPractice(practice)
        practice=Practice("PracticeInfo", self.PracticeInfo)
        self.AddPractice(practice)

    @abstractmethod
    def ToJson(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__,
            # Ensure practices is always a dictionary
            "practices": {
                practice.name: practice.ToJson() for practice in self.practices.values()
            }
            }

    @abstractmethod
    def FromJson(self, json):
        raise NotImplementedError("FromJson is not implemented")

    def UsePractice(self, practice_name, *args, **kwargs):
        # Call the practice function with the arguments
        print(f"Pit.UsePractice Using practice {practice_name} with args {args} and kwargs {kwargs}")
        #print(f"practices: {self.practices}")
        if practice_name in self.practices:
            result= self.practices[practice_name].Use(*args, **kwargs)
            #print(f"Pit.UsePractice Result: {result}")
            return result
        else:
            raise ValueError(f"practice {practice_name} not found")

    def AddPractice(self, practice: Practice):
        """
        Add a practice to the pit.
        
        Args:
            practice: Practice object to add
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        self.practices[practice.name] = practice
        return True

    def ListPractices(self, name_only=False):
        """
        List all practices of the pit.
        
        Returns:
            list: List of practice names
        """
        if name_only:
            return list(self.practices.keys())
        else:
            return {practice:self.practices[practice].ToJson() for practice in self.practices.keys()}
        
    def PracticeInfo(self, practice: str):
        """
        Get information about a specific practice.
        
        Args:
            practice_name: Name of the practice
            
        Returns:
            dict: Information about the practice
        """
        if practice not in self.practices:
            raise ValueError(f"practice {practice} not found")
        
        # if description is not set, use the docstring
        
        practice_func = self.practices[practice]
        
        # Get function signature and docstring
        import inspect
        
        if isinstance(practice_func, Callable):
            signature = str(inspect.signature(practice_func))
            docstring = practice_func.__doc__ or "No documentation available"
        else:
            signature = "No signature available"
            docstring = "No documentation available"
        
        return {
            # practice is a string
            "name": practice,
            "description": self.practices[practice].description,
            "input_schema": self.practices[practice].input_schema,
            "signature": signature,
            "docstring": docstring,
            "callable": callable(practice_func)
        }
