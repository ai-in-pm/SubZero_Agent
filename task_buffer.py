"""
Task Buffer for the SubZero Agent

This module provides a buffer for storing tasks proposed and solved by the SubZero agent.
It is used to maintain a history of tasks for reference and learning.
"""

import random
from typing import List, Any, Optional
from collections import deque

class TaskBuffer:
    """
    A buffer for storing tasks with a maximum size.
    
    When the buffer is full, adding a new task will remove the oldest one.
    """
    
    def __init__(self, max_size: int = 100):
        """
        Initialize the task buffer with the specified maximum size.
        
        Args:
            max_size: The maximum number of tasks to store in the buffer
        """
        self.max_size = max_size
        self.buffer = deque(maxlen=max_size)
    
    def add(self, task: Any) -> None:
        """
        Add a task to the buffer.
        
        If the buffer is full, the oldest task will be removed.
        
        Args:
            task: The task to add to the buffer
        """
        self.buffer.append(task)
    
    def sample(self, n: int = 1) -> List[Any]:
        """
        Sample n tasks from the buffer randomly.
        
        Args:
            n: The number of tasks to sample
            
        Returns:
            A list of sampled tasks
        """
        if not self.buffer:
            return []
        
        n = min(n, len(self.buffer))
        return random.sample(list(self.buffer), n)
    
    def get_all(self) -> List[Any]:
        """
        Get all tasks in the buffer.
        
        Returns:
            A list of all tasks in the buffer
        """
        return list(self.buffer)
    
    def clear(self) -> None:
        """
        Clear the buffer.
        """
        self.buffer.clear()
    
    def __len__(self) -> int:
        """
        Get the number of tasks in the buffer.
        
        Returns:
            The number of tasks in the buffer
        """
        return len(self.buffer)
    
    def __getitem__(self, index: int) -> Any:
        """
        Get the task at the specified index.
        
        Args:
            index: The index of the task to get
            
        Returns:
            The task at the specified index
        """
        return list(self.buffer)[index]
