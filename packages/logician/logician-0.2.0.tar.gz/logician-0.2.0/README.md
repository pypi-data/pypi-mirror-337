# Logician

**The logical choice for Python logging.** 🖖

[![PyPI version](https://img.shields.io/pypi/v/logician.svg)](https://pypi.org/project/logician/)
[![Python versions](https://img.shields.io/pypi/pyversions/logician.svg)](https://pypi.org/project/logician/)
[![PyPI downloads](https://img.shields.io/pypi/dm/logician.svg)](https://pypi.org/project/logician/)
[![License](https://img.shields.io/pypi/l/logician.svg)](https://github.com/dannystewart/logician/blob/main/LICENSE)

Logician is a powerful, colorful, and intuitive logging library for Python that makes beautiful logs easy.

## Features

- **Color-coded log levels:** Instantly identify log importance with intuitive colors.
- **Flexible formatting:** Choose between detailed or simple log formats.
- **Smart context detection:** Automatically detects logger names from classes and modules.
- **Time-aware logging:** Formats datetime objects into human-readable strings.
- **File logging:** Easily add rotating file handlers with sensible defaults.
- **Thread-safe:** Designed for reliable logging in multi-threaded applications.

## Installation

```bash
pip install logician
```

## Quick Start

```python
from logician import Logician

# Create a basic logger
logger = Logician.get_logger("MyApp")
logger.info("Application started")
logger.warning("Something seems off...")
logger.error("An error occurred!")

# With automatic name detection
class MyClass:
    def __init__(self):
        self.logger = Logician.get_logger()  # Automatically uses "MyClass" as the logger name
        self.logger.info("MyClass initialized")

# Simple format (just the message)
simple_logger = Logician.get_logger("SimpleLogger", simple=True)
simple_logger.info("This message appears without timestamp or context")

# With context information
context_logger = Logician.get_logger("ContextLogger", show_context=True)
context_logger.info("This message shows which function called it")

# Time-aware logging
from datetime import datetime
time_logger = Logician.get_logger("TimeLogger", time_aware=True)
time_logger.info("Event occurred at %s", datetime.now())  # Formats the datetime nicely

# File logging
from pathlib import Path
file_logger = Logician.get_logger("FileLogger", log_file=Path("app.log"))
file_logger.info("This message goes to both console and file")
```

## Advanced Usage

### Customizing Log Format

```python
# Different log level
logger = Logician.get_logger("DEBUG_LOGGER", level="DEBUG")
logger.debug("This debug message will be visible")

# Turning off colors (useful for CI/CD environments)
no_color_logger = Logician.get_logger("NoColor", color=False)
```

### TimeAwareLogger

The TimeAwareLogger automatically formats datetime objects in log messages:

```python
from datetime import datetime, timedelta
from logician import Logician

logger = Logician.get_logger("TimeDemo", time_aware=True)

now = datetime.now()
yesterday = now - timedelta(days=1)
next_week = now + timedelta(days=7)

logger.info("Current time: %s", now)                 # "Current time: today at 2:30 PM"
logger.info("Yesterday was: %s", yesterday)          # "Yesterday was: yesterday at 2:30 PM"
logger.info("Meeting scheduled for: %s", next_week)  # "Meeting scheduled for: Monday at 2:30 PM"
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request!

## License

This project is licensed under the LGPL-3.0 License. See the [LICENSE](https://github.com/dannystewart/logician/blob/main/LICENSE) file for details.
