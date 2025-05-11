"""
SubZero Agent: A demonstration of the Absolute Zero paradigm for AI reasoning
Based on the paper "Absolute Zero: Reinforced Self-play Reasoning with Zero Data"

This agent implements a simplified version of the Absolute Zero Reasoner (AZR)
that can propose and solve reasoning tasks without relying on external data.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv
import os
import sys
import random
import time
from typing import List, Dict, Tuple, Any, Optional
import json

# Add the parent directory to sys.path to import from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

# Import the code executor tool
from code_executor import CodeExecutorTool
from task_buffer import TaskBuffer
from task_types import TaskType, Task, DeductionTask, AbductionTask, InductionTask

class SubZeroAgent:
    """
    SubZero Agent implements the Absolute Zero paradigm for AI reasoning.

    It can:
    1. Propose reasoning tasks (as the proposer)
    2. Solve reasoning tasks (as the solver)
    3. Learn from both roles to improve reasoning capabilities

    The agent uses a code executor as the environment to validate tasks and verify solutions.
    """

    def __init__(self, model_id: str = "claude-3-7-sonnet-latest"):
        """
        Initialize the SubZero Agent with the specified model.

        Args:
            model_id: The ID of the model to use for the agent
        """
        # Create the proposer agent
        self.proposer = Agent(
            model=Claude(id=model_id),
            description="You are an expert AI researcher specializing in creating challenging reasoning tasks. "
                       "Your goal is to propose tasks that are neither too easy nor too difficult, "
                       "but provide optimal learning opportunities.",
            tools=[CodeExecutorTool()],
            instructions=[
                "Create reasoning tasks that require deep algorithmic thinking",
                "Ensure tasks are solvable but challenging",
                "Focus on tasks that involve deduction, abduction, or induction",
                "Use Python code as the medium for tasks"
            ],
            markdown=True,
        )

        # Create the solver agent
        self.solver = Agent(
            model=Claude(id=model_id),
            description="You are an expert problem solver with deep knowledge of algorithms, mathematics, and programming. "
                       "Your goal is to solve reasoning tasks by applying systematic thinking and step-by-step reasoning.",
            tools=[CodeExecutorTool(), ReasoningTools(add_instructions=True)],
            instructions=[
                "Think step by step to solve each task",
                "Explain your reasoning clearly",
                "For code-related tasks, trace through the execution carefully",
                "Verify your solutions before submitting"
            ],
            markdown=True,
        )

        # Initialize task buffers for each task type
        self.deduction_buffer = TaskBuffer(max_size=100)
        self.abduction_buffer = TaskBuffer(max_size=100)
        self.induction_buffer = TaskBuffer(max_size=100)

        # Track performance metrics
        self.metrics = {
            "proposer_rewards": [],
            "solver_rewards": [],
            "task_complexity": [],
            "task_diversity": []
        }

    def propose_task(self, task_type: TaskType, reference_examples: List[Task] = None) -> Task:
        """
        Propose a new reasoning task of the specified type.

        Args:
            task_type: The type of task to propose (deduction, abduction, or induction)
            reference_examples: Optional list of reference examples to condition the proposal

        Returns:
            A new task of the specified type
        """
        # Format reference examples for the prompt
        examples_str = ""
        if reference_examples:
            examples_str = "Here are some reference examples:\n\n"
            for i, example in enumerate(reference_examples):
                examples_str += f"Example {i+1}:\n{example.to_prompt()}\n\n"

        # Create the prompt based on the task type
        if task_type == TaskType.DEDUCTION:
            prompt = f"""
            Propose a deduction task where given a program and an input, the goal is to predict the output.

            {examples_str}

            Create a new task that is different from the examples. The task should:
            1. Involve a Python function that takes at least one input
            2. Require step-by-step reasoning to determine the output
            3. Be deterministic (same input always produces same output)
            4. Not use any external libraries or resources

            Format your response as:
            ```python
            def f(input_param):
                # Your code here
                return result
            ```

            Input: value_to_use_as_input
            """

        elif task_type == TaskType.ABDUCTION:
            prompt = f"""
            Propose an abduction task where given a program and an output, the goal is to find a valid input.

            {examples_str}

            Create a new task that is different from the examples. The task should:
            1. Involve a Python function that takes at least one input
            2. Require reverse reasoning to determine a valid input
            3. Be deterministic (same input always produces same output)
            4. Not use any external libraries or resources

            Format your response as:
            ```python
            def f(input_param):
                # Your code here
                return result
            ```

            Output: expected_output_value
            """

        elif task_type == TaskType.INDUCTION:
            prompt = f"""
            Propose an induction task where given input-output pairs, the goal is to infer the underlying function.

            {examples_str}

            Create a new task that is different from the examples. The task should:
            1. Involve a Python function that takes at least one input
            2. Require pattern recognition to determine the function
            3. Be deterministic (same input always produces same output)
            4. Not use any external libraries or resources

            Format your response as:
            ```python
            # Hidden function to be inferred
            def f(input_param):
                # Your code here
                return result
            ```

            Examples:
            Input: example_input_1 → Output: example_output_1
            Input: example_input_2 → Output: example_output_2
            Input: example_input_3 → Output: example_output_3
            """

        # Get the response from the proposer agent
        response = self.proposer.get_response(prompt)

        # Parse the response to create a task object
        # (Implementation details would depend on the actual response format)
        # For now, we'll return a placeholder task
        if task_type == TaskType.DEDUCTION:
            return DeductionTask(
                program="def f(x): return x * 2",
                input_value=5,
                output_value=10
            )
        elif task_type == TaskType.ABDUCTION:
            return AbductionTask(
                program="def f(x): return x * 2",
                input_value=5,
                output_value=10
            )
        else:  # INDUCTION
            return InductionTask(
                program="def f(x): return x * 2",
                input_output_pairs=[
                    (1, 2),
                    (2, 4),
                    (3, 6)
                ]
            )

    def solve_task(self, task: Task) -> Tuple[str, float]:
        """
        Solve a reasoning task and return the solution and reward.

        Args:
            task: The task to solve

        Returns:
            A tuple containing the solution and the reward (0 or 1)
        """
        # Create the prompt based on the task type
        if task.task_type == TaskType.DEDUCTION:
            prompt = f"""
            Solve this deduction task:

            Given the following function and input, predict the output:

            {task.to_prompt()}

            Think step by step and explain your reasoning.
            """

        elif task.task_type == TaskType.ABDUCTION:
            prompt = f"""
            Solve this abduction task:

            Given the following function and output, find a valid input:

            {task.to_prompt()}

            Think step by step and explain your reasoning.
            """

        else:  # INDUCTION
            prompt = f"""
            Solve this induction task:

            Given the following input-output pairs, infer the underlying function:

            {task.to_prompt()}

            Think step by step and explain your reasoning.
            """

        # Get the response from the solver agent
        response = self.solver.get_response(prompt, show_full_reasoning=True)

        # Verify the solution and calculate the reward
        # (Implementation details would depend on the actual response format)
        # For now, we'll return a placeholder solution and reward
        solution = response
        reward = random.choice([0, 1])  # Placeholder

        return solution, reward

    def run_self_play_iteration(self, num_tasks: int = 5) -> Dict[str, Any]:
        """
        Run one iteration of self-play, proposing and solving tasks.

        Args:
            num_tasks: Number of tasks to propose and solve in this iteration

        Returns:
            A dictionary of metrics from this iteration
        """
        iteration_metrics = {
            "proposer_rewards": [],
            "solver_rewards": [],
            "tasks": []
        }

        for _ in range(num_tasks):
            # Randomly select a task type
            task_type = random.choice(list(TaskType))

            # Get reference examples from the appropriate buffer
            if task_type == TaskType.DEDUCTION:
                reference_examples = self.deduction_buffer.sample(3)
            elif task_type == TaskType.ABDUCTION:
                reference_examples = self.abduction_buffer.sample(3)
            else:  # INDUCTION
                reference_examples = self.induction_buffer.sample(3)

            # Propose a task
            task = self.propose_task(task_type, reference_examples)

            # Calculate proposer reward (placeholder)
            proposer_reward = random.uniform(0, 1)

            # Solve the task
            solution, solver_reward = self.solve_task(task)

            # Store the task in the appropriate buffer
            if task_type == TaskType.DEDUCTION:
                self.deduction_buffer.add(task)
            elif task_type == TaskType.ABDUCTION:
                self.abduction_buffer.add(task)
            else:  # INDUCTION
                self.induction_buffer.add(task)

            # Record metrics
            iteration_metrics["proposer_rewards"].append(proposer_reward)
            iteration_metrics["solver_rewards"].append(solver_reward)
            iteration_metrics["tasks"].append({
                "type": task_type.name,
                "task": task.to_dict(),
                "solution": solution
            })

        # Update overall metrics
        self.metrics["proposer_rewards"].extend(iteration_metrics["proposer_rewards"])
        self.metrics["solver_rewards"].extend(iteration_metrics["solver_rewards"])

        return iteration_metrics

    def demonstrate(self, num_iterations: int = 3, tasks_per_iteration: int = 2):
        """
        Demonstrate the Absolute Zero paradigm by running multiple iterations of self-play.

        Args:
            num_iterations: Number of self-play iterations to run
            tasks_per_iteration: Number of tasks to propose and solve in each iteration
        """
        print("🧊 SubZero Agent: Demonstrating the Absolute Zero paradigm 🧊")
        print("=" * 80)

        for i in range(num_iterations):
            print(f"\nIteration {i+1}/{num_iterations}")
            print("-" * 40)

            # Run one iteration of self-play
            iteration_metrics = self.run_self_play_iteration(tasks_per_iteration)

            # Display results
            for j, task_data in enumerate(iteration_metrics["tasks"]):
                task_type = task_data["type"]
                proposer_reward = iteration_metrics["proposer_rewards"][j]
                solver_reward = iteration_metrics["solver_rewards"][j]

                print(f"\nTask {j+1}: {task_type}")
                print(f"Proposer Reward: {proposer_reward:.2f}")
                print(f"Solver Reward: {solver_reward:.2f}")

                # In a real implementation, we would display the actual task and solution
                # For now, we'll just print placeholders
                print("Task Details: [Task details would be displayed here]")
                print("Solution: [Solution would be displayed here]")

            # Pause between iterations
            if i < num_iterations - 1:
                print("\nMoving to next iteration...")
                time.sleep(1)

        print("\n" + "=" * 80)
        print("🧊 SubZero Agent: Demonstration complete 🧊")
        print("=" * 80)


if __name__ == "__main__":
    # Create and run the SubZero agent
    agent = SubZeroAgent()
    agent.demonstrate()
