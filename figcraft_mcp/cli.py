"""Command-line interface for FIGCRAFT-MCP."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from .config import (
    DEFAULT_PORT,
    find_figcraft_cli,
    find_figcraft_gui,
    get_default_automation_root,
    generate_mcp_config_dict,
)
from .client import FigCraftClient
from .demo import run_demo


def cmd_check(args):
    """Run diagnostics on environment, binaries, and MCP connectivity."""
    print("=" * 60)
    print("      FIGCRAFT-MCP SYSTEM & CONNECTIVITY DIAGNOSTICS")
    print("=" * 60)
    print(f"Platform           : {sys.platform} ({os.name})")
    print(f"Python             : {sys.version.split()[0]}")
    print(f"Default Auto-Root  : {get_default_automation_root()}")

    cli_path = find_figcraft_cli()
    gui_path = find_figcraft_gui()

    print(f"figcraft-cli Path  : {cli_path or '[NOT FOUND]'}")
    print(f"figcraft GUI Path  : {gui_path or '[NOT FOUND]'}")

    if not cli_path:
        print("\n[!] PERINGATAN: figcraft-cli tidak ditemukan secara otomatis.")
        print("    Harap pasang FigCraft dari https://github.com/storytold/figcraft")
        return

    # [1] Headless Mode Test
    print("\n[1] Menguji Headless MCP Server...")
    try:
        with FigCraftClient(mode="headless", cli_path=cli_path, timeout=5.0) as client:
            doc = client.inspect_document()
            if doc and not doc.get("isError"):
                print("    [✓] Headless MCP Berfungsi Normal!")
                headless_ok = True
            else:
                print("    [-] Headless MCP gagal merespons dokumen.")
                headless_ok = False
    except Exception as e:
        print(f"    [-] Gagal menguji Headless MCP: {e}")
        headless_ok = False

    # [2] Live GUI Remote Mode Test
    print(f"\n[2] Menguji Live GUI Remote (Port {args.port})...")
    try:
        with FigCraftClient(mode="live", port=args.port, cli_path=cli_path, timeout=3.0) as client:
            doc = client.inspect_document()
            if doc and not doc.get("isError"):
                print(f"    [✓] Live GUI Terhubung di port {args.port}!")
                live_ok = True
            else:
                raise ConnectionError("Aplikasi GUI tidak merespons.")
    except Exception as e:
        print(f"    [-] Standby di port {args.port}: {e}")
        print("        (Buka jendela FigCraft dengan 'start-figcraft-live.bat' untuk mode Live)")
        live_ok = False

    print("\n" + "=" * 60)
    print("RINGKASAN STATUS:")
    print(f" • Headless Mode : {'SIAP (OK)' if headless_ok else 'GAGAL'}")
    print(f" • Live GUI Mode : {'SIAP (OK)' if live_ok else 'STANDBY (Aplikasi GUI belum dibuka dengan --control ' + str(args.port) + ')'}")
    print("=" * 60)


def cmd_setup(args):
    """Generate and display or save an MCP configuration tailored to this device."""
    cli_path = find_figcraft_cli() or "figcraft-cli"
    root_path = args.root or get_default_automation_root()
    config = generate_mcp_config_dict(cli_path=cli_path, root_path=root_path, port=args.port)
    config_json = json.dumps(config, indent=2)

    if args.write:
        output_path = Path(args.write).resolve()
        output_path.write_text(config_json, encoding="utf-8")
        print(f"[✓] Konfigurasi MCP berhasil disimpan ke: {output_path}")
    else:
        print("--- Konfigurasi mcp_config.json untuk Perangkat Ini ---")
        print(config_json)
        print("\nSalin konfigurasi di atas ke file config MCP Anda (Claude Desktop, Cursor, Antigravity, dll.)")


def cmd_live(args):
    """Launch FigCraft GUI in remote control mode."""
    gui_path = find_figcraft_gui()
    if not gui_path:
        print("[-] Eksekutabel FigCraft GUI tidak ditemukan!")
        print("    Silakan atur path via environment variable FIGCRAFT_PATH.")
        sys.exit(1)

    print(f"[*] Menjalankan FigCraft GUI dengan port kontrol {args.port}...")
    print(f"    Path: {gui_path}")
    
    if sys.platform == "win32":
        subprocess.Popen([gui_path, "--control", str(args.port)], creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0)
    else:
        subprocess.Popen([gui_path, "--control", str(args.port)])
    
    print(f"[✓] FigCraft berhasil dibuka. Buka berdampingan dengan AI Agent Anda!")


def cmd_demo(args):
    """Run interactive UI drawing demo."""
    run_demo(mode=args.mode, port=args.port)


def main():
    parser = argparse.ArgumentParser(
        prog="figcraft-mcp",
        description="Universal CLI & Automation Tool for FigCraft Model Context Protocol"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # check
    p_check = subparsers.add_parser("check", help="Periksa ketersediaan binary dan uji konektivitas MCP")
    p_check.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port kontrol live GUI")

    # setup
    p_setup = subparsers.add_parser("setup", help="Hasilkan mcp_config.json otomatis untuk perangkat ini")
    p_setup.add_argument("--root", type=str, default=None, help="Folder root otomasi (default: home dir)")
    p_setup.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port kontrol live GUI")
    p_setup.add_argument("--write", "-w", type=str, default=None, help="Simpan langsung ke path file target")

    # live
    p_live = subparsers.add_parser("live", help="Buka aplikasi FigCraft GUI dalam mode remote control")
    p_live.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port kontrol remote (default: 9001)")

    # demo
    p_demo = subparsers.add_parser("demo", help="Jalankan demo perakitan kartu UI otomatis")
    p_demo.add_argument("--mode", choices=["live", "headless"], default="live", help="Mode target demo")
    p_demo.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port kontrol remote")

    args = parser.parse_args()
    if not args.command:
        cmd_check(argparse.Namespace(port=DEFAULT_PORT))
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "setup":
        cmd_setup(args)
    elif args.command == "live":
        cmd_live(args)
    elif args.command == "demo":
        cmd_demo(args)


if __name__ == "__main__":
    main()
