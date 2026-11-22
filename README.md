# FigCraft MCP: Universal AI Design & Automation Hub

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-orange.svg)](https://modelcontextprotocol.io/)

A cross-platform bridge and automation toolkit connecting **FigCraft** (the offline native vector design app) to AI coding assistants (**Antigravity**, **Claude Desktop**, **Cursor**, **Gemini CLI**, and custom agents) via the **Model Context Protocol (MCP)**.

---

## Key Features

- **Split-Screen Live Co-Designing (Port 9001):** Watch your AI agent construct wireframes, cards, and vector nodes step-by-step right before your eyes inside the running FigCraft GUI.
- **Headless Background Automation:** Execute automated design generation, asset exports (PNG/SVG/PDF), and layout validation without launching a graphical window.
- **Universal & Device-Independent:** Automatically resolves binary locations and user directories across **Windows**, **macOS**, and **Linux** without hardcoded paths.
- **Zero Third-Party Runtime Dependencies:** Runs purely using the standard Python library.

---

## Operating Modes

```
+-------------------------------------------------------+
|                    AI Assistant                       |
|   (Antigravity / Claude Desktop / Cursor / Scripts)   |
+---------------------------+---------------------------+
                            | JSON-RPC (MCP)
                            v
       +-----------------------------------------+
       |               figcraft-cli              |
       +--------------------+--------------------+
                            |
           +----------------+----------------+
           |                                 |
           v (Mode 1: --attach 9001)         v (Mode 2: headless)
+------------------------+      +------------------------+
|      FigCraft GUI      |      | In-Memory Engine Core  |
|  (Live Canvas Drawing) |      |   (Headless Builds)    |
+------------------------+      +------------------------+
```

### 1. Live Remote Mode (Interactive)
The AI agent sends instructions directly to your open FigCraft GUI canvas.
- Launch the GUI in remote control mode:
  ```bash
  # Windows
  start-figcraft-live.bat
  # or PowerShell:
  .\start-figcraft-live.ps1

  # macOS / Linux
  ./scripts/start-figcraft-live.sh

  # Or using Python CLI:
  python -m figcraft_mcp live
  ```
- Place FigCraft side-by-side with your AI chat window and request layout builds!

### 2. Headless Mode (Background & CI/CD)
The agent directly generates and queries documents in the background without needing a visible window.

---

## Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/FIGCRAFT-MCP.git
cd FIGCRAFT-MCP
```

### 2. Verify Your Setup
Run the built-in diagnostic tool to test binary detection and MCP connectivity:
```bash
python -m figcraft_mcp check
# or
python test-connection.py
```

### 3. Generate MCP Configuration
Generate a customized `mcp_config.json` tailored to your current operating system and paths:
```bash
python -m figcraft_mcp setup
```
To write it directly to a file:
```bash
python -m figcraft_mcp setup -w mcp_config.json
```

---

## Client Integration Examples

### Claude Desktop
Add the following block to your `claude_desktop_config.json`:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "figcraft-live": {
      "command": "figcraft-cli",
      "args": ["mcp", "--attach", "9001"]
    }
  }
}
```
*(If `figcraft-cli` is not on your system PATH, replace `"figcraft-cli"` with the full path outputted by `python -m figcraft_mcp setup`).*

### Antigravity & Cursor
Copy the generated configuration from `mcp_config.json` into your workspace or user MCP configuration file.

---

## Python API Usage

You can also automate FigCraft programmatically using the included Python client:

```python
from figcraft_mcp import FigCraftClient

# Connect to the live GUI canvas
with FigCraftClient(mode="live", port=9001) as client:
    # 1. Create a container frame
    frame_id = client.create_frame(
        name="Profile Card",
        x=50,
        y=50,
        width=320,
        height=180,
        props={"cornerRadius": 12, "fills": [{"type": "solid", "color": "#1E1E2E"}]}
    )

    # 2. Add an avatar badge
    client.create_ellipse(
        name="Avatar",
        x=20,
        y=20,
        width=48,
        height=48,
        parent=frame_id,
        props={"fills": [{"type": "solid", "color": "#89B4FA"}]}
    )

    # 3. Add text
    client.create_text(
        text="Alex Designer",
        name="User Name",
        x=80,
        y=32,
        parent=frame_id,
        props={"fontSize": 16, "fills": [{"type": "solid", "color": "#CDD6F4"}]}
    )
```

Run the built-in demo to see a sample card drawn in real time:
```bash
python -m figcraft_mcp demo
```

---

## Environment Variables

| Variable | Description |
| :--- | :--- |
| `FIGCRAFT_CLI_PATH` | Explicit path to `figcraft-cli` binary. |
| `FIGCRAFT_PATH` | Explicit path to `figcraft` GUI binary. |
| `FIGCRAFT_AUTOMATION_ROOT` | Custom root directory for headless file operations (default: user home directory). |

---

## License

Distributed under the [MIT License](LICENSE). Contributions, feature requests, and bug reports are welcome!
