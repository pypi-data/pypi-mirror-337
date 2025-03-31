# dotenvy-py

A Python port of Rust's dotenvy with first-occurrence-wins behavior.

## Features

- Loads environment variables from `.env` files
- Implements "first occurrence wins" behavior, matching Rust's dotenvy
- Searches for env files in parent directories
- Allows prioritized loading of multiple env files
- Fully typed with PEP 484 annotations
- 100% compatible API with Rust's dotenvy

## Installation

```bash
pip install dotenvy-py
```

## Usage

### Basic Usage

```python
import dotenvy_py

# Load .env file from current directory
env_path = dotenvy_py.dotenv()
if env_path:
    print(f"Loaded environment from: {env_path}")
else:
    print("No .env file found")
```

### Loading Specific File

```python
import dotenvy_py

# Load specific .env file
env_path = dotenvy_py.from_filename(".env.development")
if env_path:
    print(f"Loaded environment from: {env_path}")
```

### Search in Parent Directories

```python
import dotenvy_py

# Find an env file in the current or parent directories
env_path = dotenvy_py.find_upwards(".env.production")
if env_path:
    print(f"Found environment file at: {env_path}")
    # Load it
    dotenvy_py.from_filename(env_path)
```

### Priority Loading (like .env.game_client then .env)

```python
import dotenvy_py

# Load files in priority order (first file has highest priority)
loaded_files = dotenvy_py.load_with_priority([".env.game_client", ".env"])
if loaded_files:
    print(f"Loaded environment files: {', '.join(str(p) for p in loaded_files)}")
else:
    print("No environment files found")
```

## First Occurrence Wins Behavior

Unlike the standard Python `python-dotenv` library where later definitions override earlier ones, `dotenvy-py` implements the "first occurrence wins" behavior:

1. Environment variables that already exist in the process environment take precedence over variables in `.env` files
2. The first definition of a variable in a file (or across multiple files) is used, later definitions are ignored
3. This matches the behavior of Rust's `dotenvy` crate

## License

MIT 