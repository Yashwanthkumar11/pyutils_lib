# pyutils_lib

A comprehensive Python utility library that provides a robust coding framework and essential functionalities for Python applications.

## Current Features

- **Configuration Management**
- **Logging**
- **Reporting**

## Prerequisites

- Python 3.7 or higher
- pipenv (Python package manager)

## Installation & Setup

### For Development (Local Projects)

If you're working with pyutils_lib alongside other local projects:

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yashwanthkumar11/pyutils_lib.git
   cd pyutils_lib
   ```

2. **Set up the development environment**
   ```bash
   # Install dependencies and create virtual environment
   pipenv install --dev
   
   # Activate the virtual environment
   pipenv shell
   
   # Install the package in editable mode
   pip install -e . --use-pep517
   ```

### Using in Other Projects

#### Method 1: Local Development (Recommended for active development)

1. **Directory Structure**
   Ensure your project structure looks like this:
   ```
   parent_folder/
   ├── your_project/
   └── pyutils_lib/
   ```

2. **Add to your project's Pipfile**
   ```toml
   [packages]
   # ... your other dependencies
   pyutils_lib = {path = "./../pyutils_lib", editable = true}
   ```

3. **Install dependencies**
   ```bash
   cd your_project
   pipenv install --dev
   ```
   And change the interpreter in your IDE to use the created pipenv environment.

#### Method 2: Install from Source

```bash
# Install directly from the pyutils_lib directory
pip install /path/to/pyutils_lib/

# Or install in editable mode for development
pip install -e /path/to/pyutils_lib/
```

#### Method 3: Install from Built Package

```bash
# First, build the package (from pyutils_lib directory)
python -m build

# Then install the wheel file
pip install dist/pyutils_lib-1.0.0-py3-none-any.whl
```

## Usage

Once installed, you can import and use the library in your Python projects:

```python
import pyutils_lib
# or
from pyutils_lib.services.config_manager import ConfigManager
```

## Development

### Running Tests
```bash
pipenv shell
pytest
```

### Code Quality
```bash
pipenv shell
pylint pyutils_lib
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Yashwanthkumar11/pyutils_lib/LICENSE) file for details.

## Support

For issues and questions, please visit our [Issue Tracker](https://github.com/Yashwanthkumar11/pyutils_lib/issues).