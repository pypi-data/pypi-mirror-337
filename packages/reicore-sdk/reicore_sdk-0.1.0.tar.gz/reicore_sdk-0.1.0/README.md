# Rei Agent SDK (Python)

A Python SDK for interacting with the Reigent API.

## Installation

Install the package using pip:

```bash
pip install reicore_sdk
```

---

## Usage

```python
from reicore_sdk import ReiCoreSdk

# Initialize the SDK
api_key = "your-api-key"
rei_agent = ReiCoreSdk(api_key)

# Get Agent Details
agent = rei_agent.get_agent()
print("Agent Details:", agent)

# Chat Completion
message = "Hello, Rei! How are you?"
response = rei_agent.chat_completions(message)
print("Chat Completion:", response)
```

---
