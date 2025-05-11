"""
SubZero Agent: A demonstration of the Absolute Zero paradigm for AI reasoning

This package implements a simplified version of the Absolute Zero Reasoner (AZR)
described in the paper "Absolute Zero: Reinforced Self-play Reasoning with Zero Data".

The Absolute Zero paradigm enables AI systems to learn reasoning capabilities
without relying on any external data by:

1. Proposing reasoning tasks
2. Solving these tasks
3. Learning from both the proposal and solution processes

The SubZero agent demonstrates this paradigm using three fundamental modes of reasoning:
- Deduction: Given a program and input, predict the output
- Abduction: Given a program and output, find a valid input
- Induction: Given input-output pairs, infer the underlying function

The agent uses a code executor as the environment to validate tasks and verify solutions,
providing grounded feedback for learning.
"""

from .subzero_agent import SubZeroAgent
from .task_types import TaskType, Task, DeductionTask, AbductionTask, InductionTask
from .task_buffer import TaskBuffer
from .code_executor import CodeExecutorTool

__all__ = [
    'SubZeroAgent',
    'TaskType',
    'Task',
    'DeductionTask',
    'AbductionTask',
    'InductionTask',
    'TaskBuffer',
    'CodeExecutorTool'
]
