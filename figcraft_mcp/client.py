"""High-level FigCraft MCP Client supporting both Live GUI and Headless modes."""

import json
import subprocess
import time
from typing import Any, Dict, List, Optional, Union
from .config import find_figcraft_cli, get_default_automation_root, DEFAULT_PORT


class FigCraftClient:
    """Client for interacting with FigCraft via Model Context Protocol (MCP).
    
    Supports:
    - Mode Live: Connects to an existing GUI window on `--attach <port>` (default 9001).
    - Mode Headless: Runs a background session with custom read/write roots.
    """

    def __init__(
        self,
        mode: str = "live",
        port: int = DEFAULT_PORT,
        automation_root: Optional[str] = None,
        cli_path: Optional[str] = None,
        timeout: float = 10.0,
    ):
        self.mode = mode.lower()
        self.port = port
        self.timeout = timeout
        self.req_id = 0
        self.cli_path = cli_path or find_figcraft_cli()

        if not self.cli_path:
            raise FileNotFoundError(
                "figcraft-cli executable not found! Please install FigCraft or set "
                "the FIGCRAFT_CLI_PATH environment variable."
            )

        if self.mode == "live":
            cmd = [self.cli_path, "mcp", "--attach", str(self.port)]
        elif self.mode == "headless":
            root = automation_root or get_default_automation_root()
            cmd = [
                self.cli_path,
                "mcp",
                "--automation-read-root", root,
                "--automation-write-root", root
            ]
        else:
            raise ValueError(f"Unknown mode: {mode}. Expected 'live' or 'headless'.")

        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.initialize()

    def send(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a JSON-RPC 2.0 message and read the response."""
        self.req_id += 1
        msg = {
            "jsonrpc": "2.0",
            "id": self.req_id,
            "method": method,
            "params": params or {}
        }
        if not self.proc.stdin or not self.proc.stdout:
            raise RuntimeError("FigCraft MCP process standard I/O is closed.")

        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

        line = self.proc.stdout.readline()
        if not line:
            return {}
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return {"raw": line.strip()}

    def initialize(self) -> Dict[str, Any]:
        """Performs protocol handshake."""
        return self.send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "figcraft-python-client",
                "version": "0.2.0"
            }
        })

    def call_tool(self, name: str, args: Dict[str, Any], delay: float = 0.05) -> Dict[str, Any]:
        """Call any native FigCraft MCP tool by name."""
        res = self.send("tools/call", {"name": name, "arguments": args})
        if delay > 0:
            time.sleep(delay)
        return res

    def extract_node_id(self, tool_response: Dict[str, Any]) -> Optional[str]:
        """Helper to extract created node ID from a tool response."""
        content = tool_response.get("result", {}).get("content", [])
        if content and len(content) > 0:
            try:
                data = json.loads(content[0].get("text", "{}"))
                return data.get("id")
            except Exception:
                pass
        return None

    # --- High-level Design Helpers ---

    def create_node(
        self,
        node_type: str,
        name: Optional[str] = None,
        x: float = 0,
        y: float = 0,
        width: Optional[float] = None,
        height: Optional[float] = None,
        parent: Optional[str] = None,
        props: Optional[Dict[str, Any]] = None,
        text: Optional[str] = None,
        delay: float = 0.05,
    ) -> Optional[str]:
        """Generic node creator."""
        args: Dict[str, Any] = {"type": node_type}
        if name:
            args["name"] = name
        if text:
            args["text"] = text
        if x != 0:
            args["x"] = x
        if y != 0:
            args["y"] = y
        if width is not None:
            args["width"] = width
        if height is not None:
            args["height"] = height
        if parent is not None:
            args["parent"] = parent
        if props:
            args["props"] = props

        res = self.call_tool("create_node", args, delay=delay)
        return self.extract_node_id(res)

    def create_frame(
        self,
        name: str,
        x: float = 0,
        y: float = 0,
        width: float = 400,
        height: float = 300,
        parent: Optional[str] = None,
        props: Optional[Dict[str, Any]] = None,
        delay: float = 0.1,
    ) -> Optional[str]:
        """Creates a frame (container) layer."""
        return self.create_node(
            node_type="frame",
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            parent=parent,
            props=props,
            delay=delay,
        )

    def create_rect(
        self,
        name: str = "Rectangle",
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        parent: Optional[str] = None,
        props: Optional[Dict[str, Any]] = None,
        delay: float = 0.05,
    ) -> Optional[str]:
        """Creates a rectangle shape."""
        return self.create_node(
            node_type="rectangle",
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            parent=parent,
            props=props,
            delay=delay,
        )

    def create_ellipse(
        self,
        name: str = "Circle",
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        parent: Optional[str] = None,
        props: Optional[Dict[str, Any]] = None,
        delay: float = 0.05,
    ) -> Optional[str]:
        """Creates an ellipse or circle shape."""
        return self.create_node(
            node_type="ellipse",
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            parent=parent,
            props=props,
            delay=delay,
        )

    def create_text(
        self,
        text: str,
        name: Optional[str] = None,
        x: float = 0,
        y: float = 0,
        parent: Optional[str] = None,
        props: Optional[Dict[str, Any]] = None,
        delay: float = 0.05,
    ) -> Optional[str]:
        """Creates a text layer."""
        return self.create_node(
            node_type="text",
            name=name or f"Text: {text[:15]}",
            text=text,
            x=x,
            y=y,
            parent=parent,
            props=props,
            delay=delay,
        )

    def set_properties(self, node_id: str, props: Dict[str, Any], delay: float = 0.05) -> Dict[str, Any]:
        """Modifies properties of an existing node."""
        return self.call_tool("set_properties", {"id": node_id, "props": props}, delay=delay)

    def inspect_document(self) -> Dict[str, Any]:
        """Returns the full document tree as a dictionary."""
        return self.call_tool("inspect_document", {})

    def get_node(self, node_id: str) -> Dict[str, Any]:
        """Retrieves details of a specific node."""
        return self.call_tool("get_node", {"id": node_id})

    def screenshot(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Captures a screenshot of the current document."""
        args = {"path": path} if path else {}
        return self.call_tool("screenshot", args)

    def export(self, node_ids: List[str], format: str = "png", path: Optional[str] = None) -> Dict[str, Any]:
        """Exports selected nodes to png, svg, or pdf."""
        args: Dict[str, Any] = {"ids": node_ids, "format": format}
        if path:
            args["path"] = path
        return self.call_tool("export", args)

    def undo(self) -> Dict[str, Any]:
        """Undoes the previous action."""
        return self.call_tool("undo", {})

    def redo(self) -> Dict[str, Any]:
        """Redoes the previously undone action."""
        return self.call_tool("redo", {})

    def close(self):
        """Terminates the MCP server process."""
        if hasattr(self, "proc") and self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2.0)
            except Exception:
                self.proc.kill()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Backward compatibility alias
FigCraftLiveAgent = FigCraftClient
