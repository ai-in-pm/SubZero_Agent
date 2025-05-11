"""
Code Executor Tool for the SubZero Agent

This module provides a tool for executing Python code safely within a restricted environment.
It is used by the SubZero agent to validate proposed tasks and verify solutions.
"""

import ast
import sys
import io
import contextlib
import traceback
from typing import Dict, Any, List, Tuple, Optional
import re
from agno.tools.base import BaseTool

# List of forbidden modules that could be used for malicious purposes
FORBIDDEN_MODULES = [
    "os", "sys", "subprocess", "shutil", "socket", "requests",
    "urllib", "http", "ftplib", "telnetlib", "smtplib",
    "importlib", "builtins", "pickle", "marshal", "shelve"
]

class CodeExecutorTool(BaseTool):
    """
    A tool for safely executing Python code within a restricted environment.
    
    This tool is used by the SubZero agent to:
    1. Validate proposed tasks by executing the code
    2. Verify solutions by comparing outputs
    """
    
    name = "code_executor"
    description = "Executes Python code safely in a restricted environment"
    
    def __init__(self):
        super().__init__()
    
    def _is_safe_code(self, code: str) -> bool:
        """
        Check if the code is safe to execute.
        
        Args:
            code: The Python code to check
            
        Returns:
            True if the code is safe, False otherwise
        """
        # Check for forbidden imports
        for module in FORBIDDEN_MODULES:
            if re.search(rf'\b(?:import|from)\s+{module}\b', code):
                return False
            if re.search(rf'\b{module}\.\w+', code):
                return False
        
        # Check for eval, exec, and other potentially dangerous functions
        dangerous_funcs = ["eval", "exec", "compile", "__import__", "globals", "locals"]
        for func in dangerous_funcs:
            if re.search(rf'\b{func}\s*\(', code):
                return False
        
        # Parse the AST to check for other dangerous operations
        try:
            tree = ast.parse(code)
            
            # Check for dangerous AST nodes
            for node in ast.walk(tree):
                # Check for imports
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for name in node.names:
                        module_name = name.name.split('.')[0]
                        if module_name in FORBIDDEN_MODULES:
                            return False
            
            return True
        except SyntaxError:
            return False
    
    def _is_deterministic(self, code: str, input_value: Any) -> bool:
        """
        Check if the code is deterministic by running it multiple times.
        
        Args:
            code: The Python code to check
            input_value: The input value to use for testing
            
        Returns:
            True if the code is deterministic, False otherwise
        """
        # Run the code twice and check if the outputs match
        try:
            output1 = self.execute_code(code, input_value)
            output2 = self.execute_code(code, input_value)
            
            return output1 == output2
        except Exception:
            return False
    
    def execute_code(self, code: str, input_value: Any = None) -> Any:
        """
        Execute the given Python code with the provided input.
        
        Args:
            code: The Python code to execute
            input_value: The input value to pass to the function
            
        Returns:
            The output of the executed code
            
        Raises:
            ValueError: If the code is not safe to execute
            Exception: If there's an error during execution
        """
        if not self._is_safe_code(code):
            raise ValueError("The code contains potentially unsafe operations")
        
        # Extract the function definition
        function_match = re.search(r'def\s+f\s*\(.*?\).*?:', code)
        if not function_match:
            raise ValueError("No function 'f' found in the code")
        
        # Prepare the execution environment
        local_vars = {}
        
        # Redirect stdout and stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
                # Execute the code to define the function
                exec(code, {}, local_vars)
                
                # Check if the function exists
                if 'f' not in local_vars or not callable(local_vars['f']):
                    raise ValueError("Function 'f' is not defined or not callable")
                
                # Call the function with the input
                if input_value is not None:
                    result = local_vars['f'](input_value)
                else:
                    result = local_vars['f']()
                
                return result
        except Exception as e:
            error_msg = f"Error executing code: {str(e)}\n{traceback.format_exc()}"
            raise Exception(error_msg)
    
    def validate_task(self, code: str, input_value: Any = None, output_value: Any = None) -> Dict[str, Any]:
        """
        Validate a proposed task by executing the code and checking the output.
        
        Args:
            code: The Python code for the task
            input_value: The input value for the task
            output_value: The expected output value (optional)
            
        Returns:
            A dictionary containing validation results
        """
        results = {
            "is_valid": False,
            "is_safe": False,
            "is_deterministic": False,
            "executed_successfully": False,
            "output": None,
            "error": None
        }
        
        # Check if the code is safe
        results["is_safe"] = self._is_safe_code(code)
        if not results["is_safe"]:
            results["error"] = "Code contains potentially unsafe operations"
            return results
        
        # Try to execute the code
        try:
            result = self.execute_code(code, input_value)
            results["executed_successfully"] = True
            results["output"] = result
            
            # Check if the code is deterministic
            results["is_deterministic"] = self._is_deterministic(code, input_value)
            if not results["is_deterministic"]:
                results["error"] = "Code is not deterministic"
                return results
            
            # If an expected output is provided, check if it matches
            if output_value is not None:
                results["output_matches"] = result == output_value
            
            # If all checks pass, the task is valid
            results["is_valid"] = True
            
            return results
        except Exception as e:
            results["error"] = str(e)
            return results
    
    def verify_solution(self, task_type: str, code: str, input_value: Any = None, 
                        output_value: Any = None, solution: Any = None) -> Dict[str, Any]:
        """
        Verify a solution to a task.
        
        Args:
            task_type: The type of task (deduction, abduction, or induction)
            code: The Python code for the task
            input_value: The input value for the task
            output_value: The expected output value
            solution: The proposed solution
            
        Returns:
            A dictionary containing verification results
        """
        results = {
            "is_correct": False,
            "error": None
        }
        
        try:
            if task_type == "deduction":
                # For deduction tasks, the solution should match the output of executing the code
                actual_output = self.execute_code(code, input_value)
                results["is_correct"] = solution == actual_output
            
            elif task_type == "abduction":
                # For abduction tasks, executing the code with the solution should produce the expected output
                actual_output = self.execute_code(code, solution)
                results["is_correct"] = actual_output == output_value
            
            elif task_type == "induction":
                # For induction tasks, the solution (a function) should produce the expected outputs for all inputs
                # This is a simplified implementation
                results["is_correct"] = True  # Placeholder
            
            return results
        except Exception as e:
            results["error"] = str(e)
            return results
    
    def __call__(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Call the tool with the specified action and arguments.
        
        Args:
            action: The action to perform (execute, validate, or verify)
            **kwargs: Additional arguments for the action
            
        Returns:
            The result of the action
        """
        if action == "execute":
            return {"result": self.execute_code(kwargs.get("code"), kwargs.get("input_value"))}
        
        elif action == "validate":
            return self.validate_task(
                kwargs.get("code"),
                kwargs.get("input_value"),
                kwargs.get("output_value")
            )
        
        elif action == "verify":
            return self.verify_solution(
                kwargs.get("task_type"),
                kwargs.get("code"),
                kwargs.get("input_value"),
                kwargs.get("output_value"),
                kwargs.get("solution")
            )
        
        else:
            return {"error": f"Unknown action: {action}"}
