"""Interactive demo generating UI elements inside FigCraft."""

import time
from .client import FigCraftClient


def run_demo(mode: str = "live", port: int = 9001):
    """Draws a clean, solid, unslop UI component into FigCraft."""
    print(f"[*] Menghubungkan ke FigCraft (Mode: {mode.upper()})...")
    try:
        with FigCraftClient(mode=mode, port=port) as client:
            print("[+] Terhubung! Mulai merakit komponen UI...")

            # 1. Main Card Container (Solid dark surface, 1px crisp border)
            card_id = client.create_frame(
                name="Dialog_Gateway",
                x=60,
                y=48,
                width=380,
                height=220,
                props={
                    "fills": [{"type": "solid", "color": "#171C25"}],
                    "cornerRadius": 8,
                    "strokes": [{"type": "solid", "color": "#313847"}],
                    "strokeWeight": 1
                },
                delay=0.1
            )
            print(f"  [✓] Frame dibuat (ID: {card_id})")

            # 2. Status Label
            client.create_text(
                text="SYSTEM / ACTIVE",
                name="Status Label",
                x=24,
                y=24,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#7EE787"}],
                    "fontSize": 11,
                    "fontWeight": "bold"
                },
                delay=0.08
            )

            # 3. Main Title & Description
            client.create_text(
                text="Gateway Authentication",
                name="Card Title",
                x=24,
                y=48,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#F0F3F6"}],
                    "fontSize": 18,
                    "fontWeight": "bold"
                },
                delay=0.08
            )
            client.create_text(
                text="Node IPC listening on port 9001 via MCP protocol.",
                name="Card Description",
                x=24,
                y=76,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#8B949E"}],
                    "fontSize": 12
                },
                delay=0.08
            )

            # 4. Text Input Field Box (Solid neutral raised surface)
            client.create_rect(
                name="Input Box",
                x=24,
                y=112,
                width=332,
                height=36,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#1F2531"}],
                    "cornerRadius": 4,
                    "strokes": [{"type": "solid", "color": "#313847"}],
                    "strokeWeight": 1
                },
                delay=0.08
            )
            client.create_text(
                text="session_token: #f0a92b... ready",
                name="Input Placeholder",
                x=36,
                y=122,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#6E7686"}],
                    "fontSize": 12
                },
                delay=0.08
            )

            # 5. Primary Action Button (Solid Rust / International Orange Accent)
            btn_id = client.create_rect(
                name="Primary Button",
                x=24,
                y=164,
                width=110,
                height=32,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#E25624"}],
                    "cornerRadius": 4
                },
                delay=0.08
            )
            client.create_text(
                text="AUTHENTICATE",
                name="Button Text",
                x=38,
                y=173,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#FFFFFF"}],
                    "fontSize": 11,
                    "fontWeight": "bold"
                },
                delay=0.08
            )

            print("[✓] Komponen UI solid berhasil digambar di FigCraft!")
            return True
    except Exception as e:
        print(f"[-] Gagal menjalankan demo: {e}")
        return False
