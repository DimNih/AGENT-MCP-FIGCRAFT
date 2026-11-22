"""FigCraft Live Agent & Interactive Designer.
Provides a high-level API to manipulate and design nodes in FigCraft in real time.
"""

from figcraft_mcp.client import FigCraftClient, FigCraftLiveAgent
from figcraft_mcp.demo import run_demo

if __name__ == '__main__':
    print("=== FigCraft Live Designer Agent ===")
    print("Menjalankan demo komponen UI...")
    run_demo(mode="live", port=9001)
