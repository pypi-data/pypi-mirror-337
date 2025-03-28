
# Udene Python SDK

The official Python SDK for Udene Fraud Detection API.

## Installation

```bash
pip install udene-sdk
```

## Usage

```python
from udene_sdk import UdeneClient

# Initialize the client
client = UdeneClient('your_api_key')

# Get fraud metrics
metrics = client.get_metrics()
print(f"Current risk score: {metrics['risk_score']}")

# Track user interaction
client.track_interaction(
    user_id='user_123',
    action='login',
    metadata={
        'ip_address': '192.168.1.1',
        'device_id': 'device_456'
    }
)
```

## Documentation

For complete documentation, visit [https://docs.udene.net](https://docs.udene.net)

## License

MIT
