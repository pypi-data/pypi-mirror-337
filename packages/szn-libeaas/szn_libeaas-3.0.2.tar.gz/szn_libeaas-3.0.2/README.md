# szn-libeaas

Enterprise as a Service (EaaS) Python Client Library - Version 3.0.1

## Overview

The `szn-libeaas` library provides a Python client for interacting with the Enterprise as a Service API. It offers a clean, intuitive interface for managing enterprise resources through a RESTful API.

## Installation

You can install the package via pip:

```bash
pip install szn-libeaas
```

## Quick Start

```python
from szn_libeaas import Client

# Initialize the client
client = Client(api_key='your_api_key')

# Get a list of projects
projects = client.projects.list()

# Create a new user
new_user = client.users.create({
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'role': 'admin'
})

# Get analytics data
analytics = client.analytics.get_usage(
    start_date='2025-01-01',
    end_date='2025-03-31'
)
```

## Features

- Comprehensive API coverage for all EaaS endpoints
- Automatic authentication and token management
- Convenient resource managers for users, projects, tasks, and documents
- Configurable retry handling and error management
- Support for environment-based configuration
- Detailed logging and debugging options

## Documentation

For detailed documentation, please visit [https://szn-libeaas.readthedocs.io](https://szn-libeaas.readthedocs.io)

## Authentication

The library supports authentication via API key:

```python
from szn_libeaas import Client

# Authentication via API key
client = Client(api_key='your_api_key')

# Custom configuration
client = Client(
    api_key='your_api_key',
    base_url='https://api.custom-domain.com/v3',
    timeout=60,
    verify_ssl=True,
    debug=True
)
```

You can also configure the client using environment variables:

```bash
export SZN_LIBEAAS_API_KEY='your_api_key'
export SZN_LIBEAAS_BASE_URL='https://api.custom-domain.com/v3'
```

## Resource Examples

### Working with Users

```python
# List users with pagination
users = client.users.list(page=2, per_page=50)

# Get a specific user
user = client.users.get('user-123')

# Create a new user
new_user = client.users.create({
    'name': 'Jane Smith',
    'email': 'jane.smith@example.com',
    'department': 'Engineering'
})

# Update a user
updated_user = client.users.update('user-123', {
    'role': 'administrator'
})

# Delete a user
client.users.delete('user-123')
```

### Working with Projects

```python
# List all projects
projects = client.projects.list()

# Get a specific project
project = client.projects.get('project-456')

# Create a new project
new_project = client.projects.create({
    'name': 'New Product Launch',
    'description': 'Planning for Q2 product launch',
    'status': 'active'
})
```

### Analytics

```python
# Get usage statistics
usage = client.analytics.get_usage(
    start_date='2025-01-01',
    end_date='2025-03-31'
)

# Get summary report
summary = client.analytics.get_summary(period='month')
```

## Error Handling

```python
from szn_libeaas import Client, APIError

client = Client(api_key='your_api_key')

try:
    result = client.users.get('nonexistent-user')
except APIError as e:
    print(f"API Error ({e.status_code}): {e.message}")
    print(f"Request ID: {e.request_id}")
```

## Configuration Options

The client can be configured using various options:

```python
client = Client(
    api_key='your_api_key',          # API key for authentication
    base_url='https://custom.api',   # Custom API base URL
    timeout=30,                      # Request timeout in seconds
    verify_ssl=True,                 # Verify SSL certificates
    debug=False,                     # Enable debug logging
    retries=3,                       # Number of retries for failed requests
    config_file='~/config.ini'       # Path to configuration file
)
```

## License

This library is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.