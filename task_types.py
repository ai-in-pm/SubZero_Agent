"""
Task Types for the SubZero Agent

This module defines the different types of tasks that can be proposed and solved
by the SubZero agent, including deduction, abduction, and induction tasks.
"""

from enum import Enum
from typing import List, Dict, Any, Tuple, Optional
import json

class TaskType(Enum):
    """
    Enum representing the different types of reasoning tasks.
    """
    DEDUCTION = "deduction"  # Given program and input, predict output
    ABDUCTION = "abduction"  # Given program and output, find input
    INDUCTION = "induction"  # Given input-output pairs, infer program
    
class Task:
    """
    Base class for all reasoning tasks.
    """
    
    def __init__(self, task_type: TaskType):
        """
        Initialize a task with the specified type.
        
        Args:
            task_type: The type of the task
        """
        self.task_type = task_type
    
    def to_prompt(self) -> str:
        """
        Convert the task to a prompt string for the agent.
        
        Returns:
            A string representation of the task
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary for serialization.
        
        Returns:
            A dictionary representation of the task
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create a task from a dictionary.
        
        Args:
            data: A dictionary representation of the task
            
        Returns:
            A task object
        """
        raise NotImplementedError("Subclasses must implement this method")

class DeductionTask(Task):
    """
    A deduction task where given a program and an input, the goal is to predict the output.
    """
    
    def __init__(self, program: str, input_value: Any, output_value: Any):
        """
        Initialize a deduction task.
        
        Args:
            program: The Python code for the task
            input_value: The input value for the task
            output_value: The expected output value
        """
        super().__init__(TaskType.DEDUCTION)
        self.program = program
        self.input_value = input_value
        self.output_value = output_value
    
    def to_prompt(self) -> str:
        """
        Convert the task to a prompt string for the agent.
        
        Returns:
            A string representation of the task
        """
        return f"""
        ```python
        {self.program}
        ```
        
        Input: {self.input_value}
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary for serialization.
        
        Returns:
            A dictionary representation of the task
        """
        return {
            "type": self.task_type.value,
            "program": self.program,
            "input_value": self.input_value,
            "output_value": self.output_value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DeductionTask':
        """
        Create a deduction task from a dictionary.
        
        Args:
            data: A dictionary representation of the task
            
        Returns:
            A DeductionTask object
        """
        return cls(
            program=data["program"],
            input_value=data["input_value"],
            output_value=data["output_value"]
        )

class AbductionTask(Task):
    """
    An abduction task where given a program and an output, the goal is to find a valid input.
    """
    
    def __init__(self, program: str, input_value: Any, output_value: Any):
        """
        Initialize an abduction task.
        
        Args:
            program: The Python code for the task
            input_value: A valid input value for the task (for verification)
            output_value: The expected output value
        """
        super().__init__(TaskType.ABDUCTION)
        self.program = program
        self.input_value = input_value  # This is the "answer" but not shown in the prompt
        self.output_value = output_value
    
    def to_prompt(self) -> str:
        """
        Convert the task to a prompt string for the agent.
        
        Returns:
            A string representation of the task
        """
        return f"""
        ```python
        {self.program}
        ```
        
        Output: {self.output_value}
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary for serialization.
        
        Returns:
            A dictionary representation of the task
        """
        return {
            "type": self.task_type.value,
            "program": self.program,
            "input_value": self.input_value,
            "output_value": self.output_value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AbductionTask':
        """
        Create an abduction task from a dictionary.
        
        Args:
            data: A dictionary representation of the task
            
        Returns:
            An AbductionTask object
        """
        return cls(
            program=data["program"],
            input_value=data["input_value"],
            output_value=data["output_value"]
        )

class InductionTask(Task):
    """
    An induction task where given input-output pairs, the goal is to infer the underlying function.
    """
    
    def __init__(self, program: str, input_output_pairs: List[Tuple[Any, Any]]):
        """
        Initialize an induction task.
        
        Args:
            program: The Python code for the task (the "answer" but not shown in the prompt)
            input_output_pairs: A list of input-output pairs
        """
        super().__init__(TaskType.INDUCTION)
        self.program = program
        self.input_output_pairs = input_output_pairs
    
    def to_prompt(self) -> str:
        """
        Convert the task to a prompt string for the agent.
        
        Returns:
            A string representation of the task
        """
        pairs_str = "\n".join([f"Input: {inp} → Output: {out}" for inp, out in self.input_output_pairs])
        return f"""
        Examples:
        {pairs_str}
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary for serialization.
        
        Returns:
            A dictionary representation of the task
        """
        return {
            "type": self.task_type.value,
            "program": self.program,
            "input_output_pairs": self.input_output_pairs
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InductionTask':
        """
        Create an induction task from a dictionary.
        
        Args:
            data: A dictionary representation of the task
            
        Returns:
            An InductionTask object
        """
        return cls(
            program=data["program"],
            input_output_pairs=data["input_output_pairs"]
        )
