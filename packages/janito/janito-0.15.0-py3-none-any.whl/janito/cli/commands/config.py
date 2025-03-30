"""
Configuration management functions for Janito CLI.
This file is a thin wrapper around the actual implementation in janito.config.cli.commands
to maintain backward compatibility.
"""
import typer
from typing import Optional

from janito.config.cli.commands import (
    handle_reset_config,
    handle_reset_local_config,
    handle_reset_global_config,
    handle_show_config,
    handle_set_api_key,
    handle_set_local_config,
    handle_set_global_config,
    handle_config_commands
)

# Re-export all functions for backward compatibility
__all__ = [
    "handle_reset_config",
    "handle_reset_local_config",
    "handle_reset_global_config",
    "handle_show_config",
    "handle_set_api_key",
    "handle_set_local_config",
    "handle_set_global_config",
    "handle_config_commands"
]