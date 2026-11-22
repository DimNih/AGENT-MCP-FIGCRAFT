"""FIGCRAFT-MCP: Open Automation Hub & MCP Integration for FigCraft."""

__version__ = "0.2.0"
__author__ = "FigCraft Community"

from .client import FigCraftClient, FigCraftLiveAgent
from .config import (
    find_figcraft_cli,
    find_figcraft_gui,
    get_default_automation_root,
    generate_mcp_config_dict,
)

__all__ = [
    "FigCraftClient",
    "FigCraftLiveAgent",
    "find_figcraft_cli",
    "find_figcraft_gui",
    "get_default_automation_root",
    "generate_mcp_config_dict",
]
