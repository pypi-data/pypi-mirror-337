# GitHub Copilot API

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An unofficial Python wrapper for interacting with the GitHub Copilot Chat API.

## Disclaimer

This is an **unofficial** API wrapper and is not endorsed by or affiliated with GitHub or Microsoft. By using this package, you agree to comply with GitHub's terms of service and Copilot's usage policies. The maintainers of this package are not responsible for any misuse or violations. GitHub may change their API at any time which could break functionality.

**Use at your own risk and responsibility.**

## Installation

You can install the package from the local directory:

```bash
pip install .
```

Or using the PyPi build:

```bash
pip install copilotapi
```

## Requirements

- Python 3.6 or higher
- A valid GitHub account with Copilot access
- Chrome browser (for authentication)
- Required dependencies: `requests`, `selenium`, `rich`, `inquirer`

## Features

- ✅ Authentication with GitHub Copilot
- ✅ Token management (saving/loading)
- ✅ Chat thread creation and management
- ✅ Streaming message responses
- ✅ Model selection
- ✅ Rich interactive CLI interface

## Basic Usage

```python
from copilotapi.api import GithubCopilotClient

# Initialize the client
client = GithubCopilotClient()

# Authenticate (opens browser for login)
if not client.load_token_from_file():
    cookies = client.get_cookies()
    client.authenticate(cookies)
    client.save_token_to_file()

# Get available models
models = client.get_models()
model_id = models[0]["id"]  # Use first available model

# Create a thread
thread_id = client.create_new_thread()

# Send a message and get streaming response
for message in client.send_message("Write a Python function to calculate Fibonacci numbers", model_id, thread_id):
    if message["type"] == "content":
        print(message["text"], end="")
```

## CLI Usage

The package includes a command-line interface for interactive chat:

```bash
python -m copilotapi.cli
```

Or after installation:

```bash
copilot
```

### CLI Commands

- `exit` - Quit the application
- `new thread` - Start a fresh conversation
- `clear` - Clear the screen
- `help` - Show available commands

## API Reference

### GithubCopilotClient

Main client for interacting with the GitHub Copilot API.

#### Methods

| Method | Description |
|--------|-------------|
| `authenticate(cookies)` | Authenticate with GitHub Copilot |
| `get_cookies(headless=False, timeout=300)` | Get GitHub cookies via automated browser login |
| `load_token_from_file(filepath="copilot_token.txt", timeout_period=30)` | Load auth token from file |
| `save_token_to_file(filepath="copilot_token.txt")` | Save auth token to file |
| `get_models()` | Get available Copilot models |
| `create_new_thread()` | Create a new chat thread |
| `get_latest_thread()` | Get ID of the latest thread |
| `delete_thread(thread_id)` | Delete a chat thread |
| `send_message(message, model_id, thread_id=None, streaming=True)` | Send a message and stream the response |
| `get_inline_completion(prompt, language='python', max_tokens=1000, temperature=0)` | Get inline code completion |

#### Exceptions

- `CopilotAuthError` - Raised for authentication errors
- `CopilotAPIError` - Raised for API errors

## Example: Simple Chat Application

```python
from copilotapi.api import GithubCopilotClient, CopilotAuthError, CopilotAPIError

client = GithubCopilotClient()

try:
    # Authentication
    if not client.load_token_from_file():
        print("No token found. Authenticating...")
        cookies = client.get_cookies()
        client.authenticate(cookies)
        client.save_token_to_file()
        print("Authentication successful!")

    # Get models and create thread
    models = client.get_models()
    print(f"Available models: {[m['name'] for m in models]}")
    model_id = models[0]["id"]
    thread_id = client.create_new_thread()
    
    # Chat loop
    while True:
        prompt = input("\nYou: ")
        if prompt.lower() == "exit":
            break
            
        print("\nCopilot:", end=" ")
        for message in client.send_message(prompt, model_id, thread_id):
            if message["type"] == "content":
                print(message["text"], end="")
                
        print("\n" + "-" * 50)
            
except (CopilotAuthError, CopilotAPIError) as e:
    print(f"Error: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)