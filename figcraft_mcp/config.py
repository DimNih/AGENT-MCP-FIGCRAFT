"""Cross-platform configuration and path resolution for FigCraft MCP."""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional, List

DEFAULT_PORT = 9001


def get_default_automation_root() -> str:
    """Returns the user home directory as the default automation root.
    Can be overridden via FIGCRAFT_AUTOMATION_ROOT environment variable.
    """
    env_root = os.getenv("FIGCRAFT_AUTOMATION_ROOT")
    if env_root and os.path.exists(env_root):
        return str(Path(env_root).resolve())
    return str(Path.home().resolve())


def find_figcraft_cli() -> Optional[str]:
    """Finds the figcraft-cli executable across operating systems.
    
    Search order:
    1. FIGCRAFT_CLI_PATH environment variable
    2. FIGCRAFT_HOME environment variable
    3. System PATH (via shutil.which)
    4. Standard OS installation directories
    """
    # 1. Direct env override
    env_cli = os.getenv("FIGCRAFT_CLI_PATH")
    if env_cli and os.path.isfile(env_cli):
        return str(Path(env_cli).resolve())

    # 2. Home env override
    env_home = os.getenv("FIGCRAFT_HOME")
    if env_home:
        candidate = Path(env_home) / ("figcraft-cli.exe" if sys.platform == "win32" else "figcraft-cli")
        if candidate.is_file():
            return str(candidate.resolve())

    # 3. System PATH
    cli_on_path = shutil.which("figcraft-cli")
    if cli_on_path:
        return str(Path(cli_on_path).resolve())

    # 4. Standard platform directories
    candidates: List[Path] = []
    if sys.platform == "win32":
        prog_files = os.getenv("ProgramFiles", r"C:\Program Files")
        prog_files_x86 = os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local_app_data = os.getenv("LocalAppData", str(Path.home() / "AppData" / "Local"))

        candidates.extend([
            Path(prog_files) / "ArtCraft" / "FigCraft" / "figcraft-cli.exe",
            Path(prog_files) / "FigCraft" / "figcraft-cli.exe",
            Path(prog_files_x86) / "ArtCraft" / "FigCraft" / "figcraft-cli.exe",
            Path(local_app_data) / "Programs" / "FigCraft" / "figcraft-cli.exe",
            Path.home() / ".figcraft" / "bin" / "figcraft-cli.exe",
        ])
    elif sys.platform == "darwin":
        candidates.extend([
            Path("/Applications/FigCraft.app/Contents/MacOS/figcraft-cli"),
            Path.home() / "Applications/FigCraft.app/Contents/MacOS/figcraft-cli",
            Path("/usr/local/bin/figcraft-cli"),
            Path("/opt/homebrew/bin/figcraft-cli"),
            Path.home() / ".figcraft" / "bin" / "figcraft-cli",
        ])
    else:  # Linux and Unix-like
        candidates.extend([
            Path("/usr/bin/figcraft-cli"),
            Path("/usr/local/bin/figcraft-cli"),
            Path.home() / ".local" / "bin" / "figcraft-cli",
            Path.home() / ".figcraft" / "bin" / "figcraft-cli",
        ])

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate.resolve())

    return None


def find_figcraft_gui() -> Optional[str]:
    """Finds the figcraft GUI application executable across operating systems.
    
    Search order:
    1. FIGCRAFT_PATH environment variable
    2. FIGCRAFT_HOME environment variable
    3. System PATH (via shutil.which)
    4. Standard OS installation directories
    """
    env_gui = os.getenv("FIGCRAFT_PATH")
    if env_gui and os.path.isfile(env_gui):
        return str(Path(env_gui).resolve())

    env_home = os.getenv("FIGCRAFT_HOME")
    if env_home:
        candidate = Path(env_home) / ("figcraft.exe" if sys.platform == "win32" else "figcraft")
        if candidate.is_file():
            return str(candidate.resolve())

    gui_on_path = shutil.which("figcraft")
    if gui_on_path:
        return str(Path(gui_on_path).resolve())

    candidates: List[Path] = []
    if sys.platform == "win32":
        prog_files = os.getenv("ProgramFiles", r"C:\Program Files")
        prog_files_x86 = os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local_app_data = os.getenv("LocalAppData", str(Path.home() / "AppData" / "Local"))

        candidates.extend([
            Path(prog_files) / "ArtCraft" / "FigCraft" / "figcraft.exe",
            Path(prog_files) / "FigCraft" / "figcraft.exe",
            Path(prog_files_x86) / "ArtCraft" / "FigCraft" / "figcraft.exe",
            Path(local_app_data) / "Programs" / "FigCraft" / "figcraft.exe",
            Path.home() / ".figcraft" / "bin" / "figcraft.exe",
        ])
    elif sys.platform == "darwin":
        candidates.extend([
            Path("/Applications/FigCraft.app/Contents/MacOS/figcraft"),
            Path.home() / "Applications/FigCraft.app/Contents/MacOS/figcraft",
            Path("/usr/local/bin/figcraft"),
            Path("/opt/homebrew/bin/figcraft"),
        ])
    else:
        candidates.extend([
            Path("/usr/bin/figcraft"),
            Path("/usr/local/bin/figcraft"),
            Path.home() / ".local" / "bin" / "figcraft",
        ])

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate.resolve())

    return None


def generate_mcp_config_dict(cli_path: Optional[str] = None, root_path: Optional[str] = None, port: int = DEFAULT_PORT) -> dict:
    """Generates an MCP configuration dictionary ready for any user or device."""
    actual_cli = cli_path or find_figcraft_cli() or "figcraft-cli"
    actual_root = root_path or get_default_automation_root()

    return {
        "mcpServers": {
            "figcraft": {
                "command": actual_cli,
                "args": [
                    "mcp",
                    "--automation-read-root",
                    actual_root,
                    "--automation-write-root",
                    actual_root
                ]
            },
            "figcraft-live": {
                "command": actual_cli,
                "args": [
                    "mcp",
                    "--attach",
                    str(port)
                ]
            }
        }
    }
