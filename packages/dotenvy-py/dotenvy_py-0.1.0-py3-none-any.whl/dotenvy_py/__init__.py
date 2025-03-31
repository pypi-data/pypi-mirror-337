"""
dotenvy-py - A Python port of Rust's dotenvy with first-occurrence-wins behavior

This library provides environment variable loading from .env files with behavior 
that matches Rust's dotenvy library where the first occurrence of a variable wins.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Union, Set

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

def _parse_line(line: str) -> Optional[Tuple[str, str]]:
    """Parse a single line from an env file."""
    line = line.strip()
    
    # Skip empty lines and comments
    if not line or line.startswith('#'):
        return None
        
    # Check for key=value format
    if '=' not in line:
        return None
        
    # Split on first equals sign
    k, v = line.split('=', 1)
    k = k.strip()
    v = v.strip()
    
    # Remove quotes if present
    if len(v) >= 2:
        if (v[0] == v[-1] == '"') or (v[0] == v[-1] == "'"):
            v = v[1:-1]
            
    return k, v

def _load_file(dotenv_path: Union[str, Path], 
               override: bool = False, 
               existing_keys: Optional[Set[str]] = None) -> Tuple[Path, Dict[str, str], Set[str]]:
    """
    Load variables from specified env file without setting them in environment.
    
    Args:
        dotenv_path: Path to the .env file
        override: Whether to override existing variables
        existing_keys: Set of keys that are already set

    Returns:
        Tuple containing (resolved path, dictionary of parsed values, updated set of existing keys)
    """
    if isinstance(dotenv_path, str):
        dotenv_path = Path(dotenv_path)
    
    if not dotenv_path.exists():
        raise FileNotFoundError(f"Env file not found: {dotenv_path}")
        
    if existing_keys is None:
        existing_keys = set(os.environ.keys()) if not override else set()
    
    values = {}
    
    with open(dotenv_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                parsed = _parse_line(line)
                if parsed:
                    key, value = parsed
                    # Skip if key already exists (first occurrence wins)
                    if key not in existing_keys:
                        values[key] = value
                        existing_keys.add(key)
            except Exception as e:
                logger.warning(f"Error parsing line {line_num} in {dotenv_path}: {e}")
                
    return dotenv_path, values, existing_keys

def from_filename(dotenv_path: Union[str, Path], override: bool = False) -> Optional[Path]:
    """
    Load environment variables from specified file.
    
    Args:
        dotenv_path: Path to the .env file
        override: Whether to override existing variables

    Returns:
        Path object to the file if loaded successfully, None otherwise
    """
    try:
        path, values, _ = _load_file(dotenv_path, override)
        
        # Set environment variables
        for key, value in values.items():
            if override or key not in os.environ:
                os.environ[key] = value
                logger.debug(f"Set environment variable: {key}")
        
        return path
    except FileNotFoundError:
        logger.debug(f"Environment file not found: {dotenv_path}")
        return None
    except Exception as e:
        logger.warning(f"Failed to load environment from {dotenv_path}: {e}")
        return None

def dotenv(override: bool = False) -> Optional[Path]:
    """
    Load environment variables from .env file in the current directory.
    
    Args:
        override: Whether to override existing variables

    Returns:
        Path object to the .env file if loaded successfully, None otherwise
    """
    return from_filename(".env", override)

def find_upwards(filename: str = ".env", max_levels: int = 10) -> Optional[Path]:
    """
    Search for an env file in the current and parent directories.
    
    Args:
        filename: Name of the file to search for
        max_levels: Maximum number of parent directories to check

    Returns:
        Path to the file if found, None otherwise
    """
    current_dir = Path.cwd()
    
    for _ in range(max_levels):
        file_path = current_dir / filename
        if file_path.exists():
            return file_path
        
        # Check if we've reached the root
        parent_dir = current_dir.parent
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
        
    return None

def load_with_priority(filenames: List[str], override: bool = False) -> List[Path]:
    """
    Load multiple env files in priority order.
    First file has highest priority (its values will win).
    
    Args:
        filenames: List of filenames in priority order (highest first)
        override: Whether to override existing environment variables

    Returns:
        List of successfully loaded file paths
    """
    loaded_files = []
    existing_keys = set(os.environ.keys()) if not override else set()
    
    for filename in filenames:
        try:
            env_path = find_upwards(filename)
            if env_path:
                _, values, existing_keys = _load_file(env_path, override, existing_keys)
                
                # Set environment variables
                for key, value in values.items():
                    if override or key not in os.environ:
                        os.environ[key] = value
                        logger.debug(f"Set environment variable: {key}")
                
                loaded_files.append(env_path)
        except Exception as e:
            logger.warning(f"Failed to load {filename}: {e}")
    
    return loaded_files 