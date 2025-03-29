"""
Base tool implementation and interfaces.
"""

import shlex
import inspect
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """Base class for all tools."""
    
    name = None
    description = "Base tool"
    
    @abstractmethod
    def execute(self, args):
        """Execute the tool with the given arguments."""
        pass
    
    def parse_args(self, args_str):
        """Parse the argument string into a dictionary."""
        # Special case for bash tool - pass the entire string as the command
        if self.name == "bash":
            return {"command": args_str}
            
        # For other tools, use shlex to handle quoted arguments
        try:
            args_list = shlex.split(args_str)
        except Exception:
            # If shlex parsing fails, just use the raw string
            args_list = [args_str]
        
        # Get the signature of the execute method
        sig = inspect.signature(self.execute)
        params = list(sig.parameters.keys())
        
        # Create a dictionary of arguments
        args_dict = {}
        
        # Handle positional arguments
        for i, arg in enumerate(args_list):
            if i < len(params):
                args_dict[params[i]] = arg
            else:
                break
                
        return args_dict
    
    def __call__(self, args_str):
        """Call the tool with the given argument string."""
        args = self.parse_args(args_str)
        return self.execute(**args)