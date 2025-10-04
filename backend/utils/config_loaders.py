"""Configuration loader utility module.

This module provides functions for loading and caching YAML configuration files
with error handling and validation.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Union, Dict, Any
import logging
from functools import lru_cache
import yaml

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_ENV = "CONFIG_PATH"
DEFAULT_CONFIG_PATH = Path(os.getenv(DEFAULT_CONFIG_ENV, "config/config.yaml"))


class ConfigLoaderError(Exception):
    """Raised when configuration cannot be loaded or is invalid."""


def _read_yaml_file(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ConfigLoaderError(f"Config file does not exist: {path}")
    if not path.is_file():
        raise ConfigLoaderError(f"Config path is not a file: {path}")
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        raise ConfigLoaderError(f"Failed to read config file {path}: {e}") from e
    if not isinstance(data, dict):
        raise ConfigLoaderError(f"Config file {path} did not produce a mapping/dict.")
    return data


@lru_cache(maxsize=None)
def load_config(path: Union[str, Path] = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """
    Load and return configuration as a dictionary.

    The result is cached for repeated calls. Use reload_config() to clear the cache.
    """
    path = Path(path)
    logger.debug("Loading config from %s", path)
    return _read_yaml_file(path)


def reload_config(path: Union[str, Path] = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """
    Clear cache and reload configuration from disk.
    """
    load_config.cache_clear()
    return load_config(path)
