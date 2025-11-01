# Stplpy 👋

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## About

Stplpy is a Python library for programmatically interacting with StudyPlus, a Japanese social study platform.
This code is created for educational purposes and is not intended to encourage bot operations.

### Key Features

- User information retrieval and management
- Follow/unfollow operations
- Timeline retrieval (multiple types supported)
- Study record posting and deletion
- Like and comment on posts
- Profile picture updates
- **Complete type hints**
- **Custom exception classes**
- **Utility functions**
- **Comprehensive test suite**

## Installation

### Installation using pip (development version)

```bash
git clone https://github.com/kmch4n/Stplpy.git
cd Stplpy
pip install -e .
```

### Development Installation

Install with testing and code quality tools:

```bash
pip install -e ".[dev]"
```

## Requirements

This project requires Python 3.12 or higher.

## Setup

### 1. Obtaining the Token

Use Charles Proxy or similar tools to intercept StudyPlus mobile app traffic. You can find the token in the Request Header's Authorization field.
Extract only the `xxxxxx` part from `OAuth xxxxxxxx`.
**Note: This is different from the web version StudyPlus token.**

### 2. Creating `.env`

Create a `.env` file in the project root:

```env
TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Usage

### Basic Usage

```python
from stplpy import StudyPlus
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(".env")
client = StudyPlus(os.environ["TOKEN"])

# Get user information
myself = client.get_myself()
print(f"Username: {myself['username']}")

# Get timeline
timeline = client.get_followee_timeline()
print(f"Posts: {len(timeline['feeds'])}")

# Post study record
record = client.post_study_record(
    duration=3600,  # in seconds
    comment="Studied Python today!"
)
```

### Exception Handling

```python
from stplpy import StudyPlus
from stplpy.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    RateLimitError,
    APIError
)

client = StudyPlus(token)

try:
    user = client.get_user("username")
except ResourceNotFoundError:
    print("User not found")
except AuthenticationError:
    print("Authentication failed")
except RateLimitError:
    print("Rate limit reached")
except APIError as e:
    print(f"API error: {e.status_code}")
```

### Utility Functions

```python
from stplpy.utils import (
    format_study_duration,
    calculate_total_study_time,
    group_by_date
)

# Format study duration
duration = format_study_duration(7265)  # "2h 1m 5s"

# Calculate total study time
records = [{"duration": 3600}, {"duration": 1800}]
total = calculate_total_study_time(records)  # 5400

# Group by date
grouped = group_by_date(records, "record_datetime")
```

## Examples

For detailed usage examples, see [example.py](https://github.com/kmch4n/Stplpy/blob/main/example.py).

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=stplpy --cov-report=html
```

### Code Quality Checks

```bash
# Code formatting
black stplpy tests

# Linting
flake8 stplpy tests

# Type checking
mypy stplpy
```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License

## Changelog

### v0.2.0 (Latest)

- ✨ Added custom exception classes
- ✨ Complete type hint support
- ✨ Added utility functions
- ✅ Added pytest test suite
- 📦 Packaging with pyproject.toml
- 🐛 Fixed syntax errors and bugs
- 📝 Improved documentation

### v0.1.0

- Initial release
- Basic API functionality