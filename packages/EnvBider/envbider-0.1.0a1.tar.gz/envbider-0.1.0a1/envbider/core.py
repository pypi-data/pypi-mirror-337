"""Core functionality for EnvBinder.

This module provides the main decorator and type conversion logic for mapping
environment variables to Python objects.
"""

import os
from typing import Any, Type, TypeVar, get_type_hints, List, Optional, Union
from dataclasses import is_dataclass, fields
from datetime import datetime

T = TypeVar('T')

class ConfigurationError(Exception):
    """Raised when there is an error in configuration loading or parsing."""
    pass

def _convert_to_type(value: str, target_type: Type[T]) -> T:
    """Convert a string value to the target type.

    Args:
        value: The string value to convert.
        target_type: The type to convert to.

    Returns:
        The converted value.

    Raises:
        ConfigurationError: If the value cannot be converted to the target type.
    """
    try:
        # Handle None values
        if value is None or value == '':
            if target_type == datetime or target_type == type(None) or target_type is None:
                return None

        # Handle Optional types
        origin = getattr(target_type, "__origin__", None)
        if origin is not None:
            if origin is Optional or origin is Union and type(None) in target_type.__args__:
                if not value:
                    return None
                inner_type = next(t for t in target_type.__args__ if t is not type(None))
                return _convert_to_type(value, inner_type)
            elif origin is list:
                return value.split(',') if value else []

        if target_type == bool:
            return value.lower() in ('true', '1', 't', 'yes', 'y')
        elif target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        elif target_type == str:
            return value
        elif target_type == datetime:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            raise ConfigurationError(f"Unsupported type: {target_type}")


    except ValueError as e:
        raise ConfigurationError(f"Could not convert value '{value}' to {target_type}: {str(e)}")

def _get_env_var_name(attr_name: str) -> str:
    """Convert a Python attribute name to an environment variable name.

    Args:
        attr_name: The attribute name in snake_case.

    Returns:
        The environment variable name in UPPER_SNAKE_CASE.
    """
    return attr_name.upper()

def env_binder(cls=None, *, prefix=None):
    """Decorator that automatically binds environment variables to class attributes.

    Args:
        cls: The class to decorate.
        prefix: Optional custom prefix for environment variables. If not provided,
               the class attributes will be used as prefixes.

    Returns:
        The decorated class.

    Raises:
        ConfigurationError: If required environment variables are missing or if type conversion fails.
    """
    def decorator(cls):
        original_init = cls.__init__
        
        # Store the custom prefix as a class attribute
        cls._env_prefix = prefix

        def __init__(self, *args, **kwargs):
            # Initialize the object with default values first
            original_init(self, *args, **kwargs)
            
            type_hints = get_type_hints(cls)

            for attr_name, attr_type in type_hints.items():
                # Use custom prefix if provided, otherwise use the attribute name
                if hasattr(cls, '_env_prefix') and cls._env_prefix is not None:
                    env_prefix = f"{cls._env_prefix}_{_get_env_var_name(attr_name)}"
                else:
                    env_prefix = _get_env_var_name(attr_name)
                env_value = os.environ.get(env_prefix)

                # Check if the attribute has a default value
                has_default = hasattr(cls, attr_name)
                default_value = getattr(cls, attr_name, None) if has_default else None

                # Handle nested configuration objects
                if hasattr(attr_type, '__annotations__'):
                    # Determine the prefix for the nested object
                    # If the parent has a custom prefix, use it as a base for the nested prefix
                    if hasattr(cls, '_env_prefix') and cls._env_prefix is not None:
                        nested_prefix = f"{cls._env_prefix}_{_get_env_var_name(attr_name)}"
                    else:
                        nested_prefix = env_prefix
                    
                    # Check if the nested class has its own custom prefix
                    nested_custom_prefix = getattr(attr_type, '_env_prefix', None)
                    if nested_custom_prefix is not None:
                        # Use the nested class's custom prefix instead
                        nested_prefix = nested_custom_prefix
                    
                    # If we have environment variables for the nested object
                    nested_env_vars_exist = False
                    for nested_attr in get_type_hints(attr_type):
                        nested_env_var = f"{nested_prefix}_{_get_env_var_name(nested_attr)}"
                        if nested_env_var in os.environ:
                            nested_env_vars_exist = True
                            break
                    
                    # If we have nested environment variables, create the nested object
                    if nested_env_vars_exist:
                        # Create a new environment for the nested object
                        nested_env = {}
                        for nested_attr in get_type_hints(attr_type):
                            nested_env_var = f"{nested_prefix}_{_get_env_var_name(nested_attr)}"
                            if nested_env_var in os.environ:
                                # Store in a temporary dict with the correct key for the nested object
                                nested_env[_get_env_var_name(nested_attr)] = os.environ[nested_env_var]
                        
                        # Save original environment
                        original_env = os.environ.copy()
                        
                        try:
                            # Set the temporary environment for nested object initialization
                            os.environ.update(nested_env)
                            nested_obj = attr_type()
                            setattr(self, attr_name, nested_obj)
                        finally:
                            # Restore original environment
                            os.environ.clear()
                            os.environ.update(original_env)
                    continue

                # Special handling for datetime fields with None default
                if attr_type == datetime and default_value is None and (env_value is None or env_value == ''):
                    setattr(self, attr_name, None)
                    continue
                
                # Handle case where the field is a datetime and has a None value set explicitly
                if attr_type == datetime and getattr(self, attr_name) is None and (env_value is None or env_value == ''):
                    # Keep it as None
                    continue

                # Handle regular fields
                if env_value is None:
                    if not has_default:
                        raise ConfigurationError(f"Required environment variable {env_prefix} is not set")
                    # Keep the default value that was set by the original init
                else:
                    converted_value = _convert_to_type(env_value, attr_type)
                    setattr(self, attr_name, converted_value)

        cls.__init__ = __init__
        return cls
    
    # Handle both @env_binder and @env_binder(prefix="DB") forms
    if cls is None:
        # Called with parameters: @env_binder(prefix="DB")
        return decorator
    else:
        # Called without parameters: @env_binder
        return decorator(cls)