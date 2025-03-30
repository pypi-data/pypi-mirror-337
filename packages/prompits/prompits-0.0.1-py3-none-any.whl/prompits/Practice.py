# Practice is not a Pit
# contains a function can be used by other agents

import asyncio
import inspect
from typing import Callable


class Practice():
    def __init__(self, name:str, function: Callable, input_schema:dict=None, description:str=None, parameters:dict=None, is_async:bool=False):
        self.name=name
        self.description=description
        self.function=function
        self.parameters=parameters
        self.input_schema=input_schema
        self.is_async=is_async

    def Use(self, *args, **kwargs):
        # call function return result
        #print(f"Calling function {self.name} with args {args} and kwargs {kwargs}")
        if self.is_async:
            #print(f"Calling async function {self.name}")
            if self.parameters:
                # merge parameters with kwargs
                kwargs.update(self.parameters)
                print(f"Calling async function {self.name} with args {args} and kwargs {kwargs}")
                return asyncio.run(self.function(*args, **kwargs))
            else:
                print(f"Calling async function {self.name} with args {args} and kwargs {kwargs}")
                return asyncio.run(self.function(*args, **kwargs))
        else:
            print(f"Calling sync function {self.name}")
            if self.parameters:
                # merge parameters with kwargs
                kwargs.update(self.parameters)
                return self.function(*args, **kwargs)
            else:
                return self.function(*args, **kwargs)

    def Info(self):
        # return function signature and docstring
        if self.description:
            return self.description
        else:
            return self.function.__doc__

    def ToJson(self):
        return {
            "name": self.name,
            "description": self.description,
            # get signature of the function
            "signature": str(inspect.signature(self.function)),
            "docstring": self.function.__doc__,
            "input_schema": self.input_schema,
            "args": self.function.__code__.co_varnames[:self.function.__code__.co_argcount]
        }
        
    
    def FromJson(self, json):
        self.name=json["name"]
        self.description=json["description"]
        self.function=json["function"]
        self.args=json["args"]
