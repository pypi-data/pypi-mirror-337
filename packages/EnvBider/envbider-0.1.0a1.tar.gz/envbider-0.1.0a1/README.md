# EnvBider

A Python library for simplified environment variable management with type conversion and nested configuration support.

## Features

- Simple environment variable access with type conversion
- Nested configuration support
- Automatic environment file (.env) loading
- Validation and default values

## Installation

```bash
pip install EnvBider
```

## Basic Usage

```python
import envbider

# Load environment variables from .env file
envbider.load_dotenv()

# Get environment variable with type conversion
port = envbider.get('PORT', default=8000, type=int)
debug = envbider.get('DEBUG', default=False, type=bool)

# Nested configuration
config = envbider.get_nested('APP_CONFIG')
print(config['database']['host'])
```

## Advanced Usage

### Type Conversion

```python
# Automatic type conversion
value = envbider.get('SOME_NUMBER', type=float)
```

### Nested Configuration

```python
# JSON string in environment variable
config = envbider.get_nested('APP_CONFIG')

# Access nested values
print(config['logging']['level'])
```

### Custom Prefixes

```python
from envbider.core import env_binder

# Define nested configuration classes with custom prefixes
@env_binder(prefix="DB")
class DatabaseConfig:
    host: str
    port: int = 5432
    username: str
    password: str

@env_binder
class AppConfig:
    app_name: str
    database: DatabaseConfig = None

# Environment variables would be:
# APP_NAME=MyApp
# DB_HOST=localhost
# DB_PORT=5432
# DB_USERNAME=admin
# DB_PASSWORD=secret
```

### Validation

```python
# Validate required variables
envbider.validate_required(['DB_HOST', 'DB_PORT'])
```

## Demonstration

1. Create a `.env` file:
```
PORT=8080
DEBUG=true
APP_CONFIG={"database": {"host": "localhost", "port": 5432}, "logging": {"level": "info"}}
```

2. Run the example:
```python
import envbider

envbider.load_dotenv()

port = envbider.get('PORT', type=int)
debug = envbider.get('DEBUG', type=bool)
config = envbider.get_nested('APP_CONFIG')

print(f"Port: {port}")
print(f"Debug mode: {debug}")
print(f"Database host: {config['database']['host']}")
```

## License

MIT