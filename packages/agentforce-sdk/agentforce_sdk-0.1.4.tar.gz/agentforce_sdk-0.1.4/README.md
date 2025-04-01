# Salesforce AgentForce SDK

[![PyPI version](https://badge.fury.io/py/agentforce.svg)](https://badge.fury.io/py/agentforce)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for creating, managing, and deploying AI agents in Salesforce.

## Introduction

The Salesforce AgentForce SDK provides a programmatic interface to Salesforce's Agent infrastructure, allowing developers to define and interact with agents using Python code.

## Installation

```bash
pip install agentforce-sdk
```

## Documentation

Comprehensive documentation for the SDK is available in the [docs](docs) directory:

- [API Documentation](docs/api_documentation.md): Detailed documentation for all SDK components, classes, and methods.
- [JSON Schemas](docs/schemas): JSON schemas for validating agent definitions in various formats.

## Directory Structure Support

The SDK supports multiple formats for defining agents:

1. **Single JSON File**: A complete agent definition in a single JSON file.
2. **Nested Directory Structure**: A hierarchical directory structure with topics and actions in subdirectories.
3. **Modular Directory Structure**: A flat directory structure with references between components.

For more information, see the [Directory Structures section](docs/api_documentation.md#directory-structures) in the API documentation.

## Examples

The [examples](examples) directory contains sample code demonstrating how to use the SDK:

- [Creating an agent programmatically](examples/create_agent_programmatically.py)
- [Creating an agent from a JSON file](examples/create_agent_from_json_file.py)
- [Creating an agent from a nested directory](examples/create_agent_from_nested_directory.py)
- [Creating an agent from a modular directory](examples/create_agent_from_modular_directory.py)
- [Running an agent](examples/run_agent.py)
- [Exporting an agent](examples/export_salesforce_agent_example.py)

## Quick Start

```python
from agent_sdk import Agentforce
from agent_sdk.models import Agent, Topic, Action, Input, Output

# Initialize the client
client = Agentforce(username="your_username", password="your_password")

# Create a simple agent
agent = Agent(
    name="Hello World Agent",
    description="A simple agent that says hello",
    agent_type="Bot",
    company_name="Salesforce"
)

# Add a topic
topic = Topic(
    name="Greetings",
    description="Handle greetings",
    scope="Handle greeting requests"
)

# Add an action
action = Action(
    name="SayHello",
    description="Say hello to the user",
    inputs=[
        Input(
            name="name",
            description="Name of the person to greet",
            data_type="String",
            required=True
        )
    ],
    example_output=Output(
        status="success",
        details={"message": "Hello, World!"}
    )
)

# Add the action to the topic
topic.actions = [action]

# Add the topic to the agent
agent.topics = [topic]

# Create the agent in Salesforce
result = client.create(agent)
print(f"Agent created with ID: {result['id']}")
```

## IDE Integration

The SDK includes JSON schema files that can help with IDE integration:

- VSCode: Use the schemas to validate your agent definition files
- Cursor: Leverage the detailed API documentation for intelligent code completion
- WindSurf: Use the schema files to provide structured editing experiences

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 