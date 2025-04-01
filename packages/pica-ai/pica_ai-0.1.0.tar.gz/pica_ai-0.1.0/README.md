# pica-ai

A Python client for interacting with the Pica API. This package helps with getting connections, actions, and system prompts for Pica.

## Installation

```bash
pip install pica-ai
```

## Requirements

- Python 3.7+
- A Pica API secret key

## Usage

### Basic Usage

```python
import os
from pica_ai import PicaClient, PicaClientOptions

# Initialize the client with your Pica secret
pica = PicaClient(
    secret=os.environ.get("PICA_SECRET"), 
    options=PicaClientOptions(
        connectors=["*"]
    )
)

# Get available connections
connections = pica.get_connections()
print(connections)

# Get available actions for a platform
available_actions = pica.get_available_actions("gmail")
print(available_actions)

# Generate a system prompt
system_prompt = pica.generate_system_prompt()
print(system_prompt)
```

### Advanced Configuration

You can customize the client behavior using options:

```python
from pica_ai import PicaClient, PicaClientOptions

options = PicaClientOptions(
    # server_url="https://custom-api.picaos.com",
    # connectors=["gmail-connection-key-1", "slack-connection-key-2"],
    # identity="user-123",
    # identity_type="user",
    # authkit=True
)

pica = PicaClient(secret="your-secret-key", options=options)
```

## Features

- Get available connections for your Pica account
- Get available actions for a platform
- Generate system prompts for LLMs

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/picahq/pica-ai.git
cd pica-ai

# Install in development mode
pip install -e .
```

### Running Examples

Get a Pica secret from the [Pica dashboard](https://app.picaos.com/settings/api-keys).

```bash
# Set your Pica secret
export PICA_SECRET=your-secret-key

# Run the basic example
python examples/basic.py
```

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
