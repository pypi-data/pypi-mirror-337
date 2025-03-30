# AIAF - AI Agent Firewall 🚀

AIAF is a security layer that prevents prompt injection and adversarial attacks on AI chatbots.

## Features

- Pattern-based detection of malicious inputs
- OpenAI moderation integration
- Comprehensive security logging
- Protection against prompt injection attacks
- Unicode obfuscation detection
- Leetspeak variation detection

## Installation

```sh
pip install aiaf
```

## Usage

```python
from aiaf import AIAF

# Initialize with your OpenAI API key
aiaf = AIAF(api_key="your-api-key")

# Check user input
result = aiaf.sanitize_input("user input here")

# View security logs
logs = aiaf.get_security_logs()
```

## Security Logging

AIAF automatically logs all security incidents to a file named "security_incidents.log" by default. The logs include:
- Timestamp of each incident
- Type of detection (pattern-based or OpenAI moderation)
- The malicious input that was blocked
- The pattern that matched (for pattern-based detections)
- Categories that were flagged (for OpenAI moderation)
- Any errors that occurred during security checks

## License

MIT License
