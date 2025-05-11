# SubZero Agent

A demonstration of the Absolute Zero paradigm for AI reasoning, based on the paper "Absolute Zero: Reinforced Self-play Reasoning with Zero Data".

## Overview

The SubZero agent implements a simplified version of the Absolute Zero Reasoner (AZR) described in the paper. It demonstrates how an AI system can learn reasoning capabilities without relying on any external data by:

1. **Proposing reasoning tasks** that maximize learning potential
2. **Solving these tasks** to improve reasoning abilities
3. **Learning from both roles** to enhance general reasoning capabilities

The agent uses a code executor as the environment to validate tasks and verify solutions, providing grounded feedback for learning.

## Key Components

The SubZero agent consists of the following key components:

- **SubZero Agent**: The main agent that implements the Absolute Zero paradigm
- **Task Types**: Three fundamental modes of reasoning:
  - **Deduction**: Given a program and input, predict the output
  - **Abduction**: Given a program and output, find a valid input
  - **Induction**: Given input-output pairs, infer the underlying function
- **Code Executor**: A tool for safely executing Python code to validate tasks and verify solutions
- **Task Buffer**: A buffer for storing tasks proposed and solved by the agent

## Installation

### Automatic Setup

The easiest way to set up the SubZero agent is to use the provided setup script:

```bash
cd subzero_agent
python setup.py
```

This script will:
1. Create a virtual environment
2. Install the required dependencies
3. Create a `.env` file from the example file

After running the setup script, you'll need to activate the virtual environment:

#### On Windows:
```bash
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
source venv/bin/activate
```

### Manual Setup

If you prefer to set up the environment manually:

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/agno-main.git
cd agno-main
```

2. Create and activate a virtual environment:

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r subzero_agent/requirements.txt
```

### Setting Up API Keys

For the full demo that uses the Agno framework and Claude model, you'll need to set up an API key:

1. Copy the example `.env` file:

```bash
cp subzero_agent/.env.example .env
```

2. Edit the `.env` file and replace `your_api_key_here` with your actual Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key
```

You can obtain an API key from [Anthropic's website](https://www.anthropic.com/).

Alternatively, you can create the `.env` file manually in the root directory of the project.

## Usage

### Running the Demo

There are two demo options available:

#### Simple Demo (No Dependencies)

To see a simplified demonstration of the Absolute Zero paradigm without any dependencies:

```bash
cd subzero_agent
python simple_demo.py
```

This will show examples of:
- Task proposal for each reasoning mode
- Task solving for each reasoning mode
- A simulated self-play iteration

#### Full Demo (Requires Agno Framework)

To run the full SubZero agent demonstration (requires the Agno framework and API keys):

```bash
cd subzero_agent
python demo.py
```

This will demonstrate:
- Task proposal for each reasoning mode
- Task solving for each reasoning mode
- A simplified self-play iteration

### Using the SubZero Agent

To use the SubZero agent in your own code:

```python
from subzero_agent import SubZeroAgent

# Create the SubZero agent
agent = SubZeroAgent()

# Run a self-play iteration
iteration_metrics = agent.run_self_play_iteration(num_tasks=5)

# Demonstrate the agent
agent.demonstrate(num_iterations=3, tasks_per_iteration=2)
```

## Implementation Details

### Proposer Role

The proposer role is responsible for generating reasoning tasks that maximize learning potential. It:

1. Receives reference examples from the task buffer
2. Proposes a new task that is different from the examples
3. Receives a reward based on the learnability of the task

### Solver Role

The solver role is responsible for solving the proposed tasks. It:

1. Receives a task from the proposer
2. Applies systematic reasoning to solve the task
3. Receives a reward based on the correctness of the solution

### Learning Mechanism

In a full implementation of the Absolute Zero paradigm, both the proposer and solver roles would be trained using reinforcement learning, with rewards based on:

- **Proposer Reward**: Encourages tasks of appropriate difficulty (neither too easy nor impossible)
- **Solver Reward**: Binary reward based on solution correctness

This implementation provides a simplified demonstration of the paradigm without the full reinforcement learning component.

## Relation to the Absolute Zero Paper

This implementation is inspired by the Absolute Zero paradigm described in the paper, but is simplified for demonstration purposes. The key concepts demonstrated include:

1. **Self-contained learning**: The agent proposes and solves its own tasks without external data
2. **Three reasoning modes**: Deduction, abduction, and induction as complementary learning signals
3. **Code as the environment**: Using code execution for task validation and solution verification
4. **Dual roles**: The proposer and solver roles working together to improve reasoning capabilities

For a full understanding of the Absolute Zero paradigm, please refer to the original paper.

## Demo Output

Below is the output from running the simple demo, which demonstrates the Absolute Zero paradigm in action:

```
================================================================================
🧊 SubZero Agent: Demonstrating the Absolute Zero Paradigm 🧊
================================================================================

    The Absolute Zero paradigm enables AI systems to learn reasoning capabilities
    without relying on any external data. Instead, the system:

    1. Proposes its own reasoning tasks
    2. Solves these tasks
    3. Learns from both the proposal and solution processes

    This demonstration will show how the SubZero agent implements this paradigm
    using three fundamental modes of reasoning:

    - DEDUCTION: Given a program and input, predict the output
    - ABDUCTION: Given a program and output, find a valid input
    - INDUCTION: Given input-output pairs, infer the underlying function

    The agent uses a code executor as the environment to validate tasks and
    verify solutions, providing grounded feedback for learning.


------------------------------------------------------------
📌 Task Proposal Demonstration
------------------------------------------------------------

    The SubZero agent can propose three types of reasoning tasks:
    - Deduction tasks: Given a program and input, predict the output
    - Abduction tasks: Given a program and output, find a valid input
    - Induction tasks: Given input-output pairs, infer the underlying function

    Let's see examples of each type of task proposal:


🔍 Task Type: DEDUCTION
📋 Task Prompt:

        ```python
        def f(numbers):
            result = []
            for i in range(len(numbers)):
                count = 0
                for j in range(len(numbers)):
                    if numbers[j] < numbers[i]:
                        count += 1
                result.append(count)
            return result
        ```

        Input: [5, 2, 6, 1, 3]


This deduction task requires the solver to trace through the code execution step by step.

🔍 Task Type: ABDUCTION
📋 Task Prompt:

        ```python
        def f(s):
            vowels = 'aeiou'
            result = ''
            for char in s:
                if char.lower() in vowels:
                    result += char.upper()
                else:
                    result += char.lower()
            return result
        ```

        Output: "hEllO wOrld"


This abduction task requires the solver to reverse-engineer an input that produces the given output.

🔍 Task Type: INDUCTION
📋 Task Prompt:

        Examples:
        Input: 0 → Output: 0
        Input: 1 → Output: 1
        Input: 2 → Output: 1
        Input: 3 → Output: 2
        Input: 4 → Output: 3
        Input: 5 → Output: 5


This induction task requires the solver to recognize the Fibonacci sequence pattern.

------------------------------------------------------------
📌 Task Solving Demonstration
------------------------------------------------------------

    The SubZero agent can solve the tasks it proposes using systematic reasoning.
    Let's see examples of solving each type of task:


🧩 Solution:

        To solve this task, I need to trace through the execution of the function with the given input.

        The function takes a list of numbers and returns a list where each element is the count of numbers
        in the original list that are less than the current number.

        Given input: [5, 2, 6, 1, 3]

        Let's trace through the execution:

        For i=0 (numbers[0] = 5):
          Count numbers less than 5: 2, 1, 3 (three numbers)
          result = [3]

        For i=1 (numbers[1] = 2):
          Count numbers less than 2: 1 (one number)
          result = [3, 1]

        For i=2 (numbers[2] = 6):
          Count numbers less than 6: 5, 2, 1, 3 (four numbers)
          result = [3, 1, 4]

        For i=3 (numbers[3] = 1):
          Count numbers less than 1: none (zero numbers)
          result = [3, 1, 4, 0]

        For i=4 (numbers[4] = 3):
          Count numbers less than 3: 2, 1 (two numbers)
          result = [3, 1, 4, 0, 2]

        Therefore, the output is [3, 1, 4, 0, 2]

🏆 Reward: 1.00

🧩 Solution:

        To solve this task, I need to find an input string that, when processed by the function, produces the output "hEllO wOrld".

        The function transforms a string by:
        - Converting vowels (a, e, i, o, u) to uppercase
        - Converting non-vowels to lowercase

        Given output: "hEllO wOrld"

        Let's work backwards:
        - 'h' is lowercase, so the original character was not a vowel (could be 'h' or 'H')
        - 'E' is uppercase, so the original character was a vowel ('e' or 'E')
        - 'l' is lowercase, so the original character was not a vowel ('l' or 'L')
        - 'l' is lowercase, so the original character was not a vowel ('l' or 'L')
        - 'O' is uppercase, so the original character was a vowel ('o' or 'O')
        - ' ' remains a space
        - 'w' is lowercase, so the original character was not a vowel ('w' or 'W')
        - 'O' is uppercase, so the original character was a vowel ('o' or 'O')
        - 'r' is lowercase, so the original character was not a vowel ('r' or 'R')
        - 'l' is lowercase, so the original character was not a vowel ('l' or 'L')
        - 'd' is lowercase, so the original character was not a vowel ('d' or 'D')

        One possible input is "Hello World"

🏆 Reward: 1.00

🧩 Solution:

        To solve this task, I need to identify the pattern in the given input-output pairs:

        (0, 0)
        (1, 1)
        (2, 1)
        (3, 2)
        (4, 3)
        (5, 5)

        Looking at the sequence of outputs: 0, 1, 1, 2, 3, 5

        This is the Fibonacci sequence, where each number is the sum of the two preceding ones:
        - f(0) = 0
        - f(1) = 1
        - f(2) = f(1) + f(0) = 1 + 0 = 1
        - f(3) = f(2) + f(1) = 1 + 1 = 2
        - f(4) = f(3) + f(2) = 2 + 1 = 3
        - f(5) = f(4) + f(3) = 3 + 2 = 5

        Therefore, the function can be implemented as:

        ```python
        def f(n):
            if n <= 1:
                return n
            return f(n-1) + f(n-2)
        ```

        This is a recursive implementation of the Fibonacci sequence.

🏆 Reward: 1.00

------------------------------------------------------------
📌 Self-Play Demonstration
------------------------------------------------------------

    In the Absolute Zero paradigm, the agent engages in self-play by:
    1. Proposing tasks that maximize learning potential
    2. Solving these tasks to improve reasoning abilities
    3. Learning from both the proposal and solution processes

    Let's simulate a self-play iteration:


🔄 Simulating self-play iteration...

📊 Self-Play Iteration Results:

Task 1: DEDUCTION
Proposer Reward: 0.75
Solver Reward: 1.00

Task 2: ABDUCTION
Proposer Reward: 0.82
Solver Reward: 0.00

Task 3: INDUCTION
Proposer Reward: 0.65
Solver Reward: 1.00

------------------------------------------------------------
📌 Conclusion
------------------------------------------------------------

    The SubZero agent demonstrates the Absolute Zero paradigm by:

    1. Proposing diverse reasoning tasks without external data
    2. Solving these tasks using systematic reasoning
    3. Learning from both the proposal and solution processes

    This approach enables continuous improvement of reasoning capabilities
    without relying on human-curated datasets, addressing scalability concerns
    in current reasoning model training approaches.

    The three reasoning modes (deduction, abduction, and induction) provide
    complementary learning signals that enhance general reasoning abilities.


================================================================================
🧊 SubZero Agent: Demonstration Complete 🧊
================================================================================
```

## Requirements

- Python 3.7+
- Agno framework (for full demo only)
- Anthropic API key (for full demo only)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
