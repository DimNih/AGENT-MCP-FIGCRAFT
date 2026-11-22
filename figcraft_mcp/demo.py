"""Interactive demo generating UI elements inside FigCraft."""

import time
from .client import FigCraftClient


def run_demo(mode: str = "live", port: int = 9001):
    """Draws a clean modern UI card component into FigCraft."""
    print(f"[*] Menghubungkan ke FigCraft (Mode: {mode.upper()})...")
    try:
        with FigCraftClient(mode=mode, port=port) as client:
            print("[+] Terhubung! Mulai merakit komponen UI...")

            # 1. Main Card Container (Glassmorphism / Modern Card)
            card_id = client.create_frame(
                name="Analytics Card",
                x=100,
                y=100,
                width=360,
                height=220,
                props={
                    "fills": [{"type": "solid", "color": "#1E1E2E"}],
                    "cornerRadius": 16,
                    "strokes": [{"type": "solid", "color": "#313244"}],
                    "strokeWeight": 1
                },
                delay=0.1
            )
            print(f"  [✓] Frame Utama dibuat (ID: {card_id})")

            # 2. Status Badge / Icon Pill
            badge_id = client.create_rect(
                name="Badge Background",
                x=24,
                y=24,
                width=80,
                height=28,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#A6E3A133"}],
                    "cornerRadius": 14
                },
                delay=0.08
            )
            client.create_text(
                text="● ACTIVE",
                name="Badge Text",
                x=36,
                y=30,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#A6E3A1"}],
                    "fontSize": 11,
                    "fontWeight": "bold"
                },
                delay=0.08
            )

            # 3. Main Metric Title & Number
            client.create_text(
                text="Monthly Active Users",
                name="Card Title",
                x=24,
                y=70,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#A6ADC8"}],
                    "fontSize": 13
                },
                delay=0.08
            )
            client.create_text(
                text="128,450",
                name="Card Value",
                x=24,
                y=95,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#CDD6F4"}],
                    "fontSize": 28,
                    "fontWeight": "bold"
                },
                delay=0.08
            )

            # 4. Progress / Growth Indicator
            client.create_rect(
                name="Progress Track",
                x=24,
                y=150,
                width=312,
                height=8,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#313244"}],
                    "cornerRadius": 4
                },
                delay=0.08
            )
            client.create_rect(
                name="Progress Fill",
                x=24,
                y=150,
                width=230,
                height=8,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#89B4FA"}],
                    "cornerRadius": 4
                },
                delay=0.08
            )
            client.create_text(
                text="+18.4% dari bulan lalu",
                name="Growth Text",
                x=24,
                y=170,
                parent=card_id,
                props={
                    "fills": [{"type": "solid", "color": "#A6E3A1"}],
                    "fontSize": 12
                },
                delay=0.08
            )

            print("[★] Demo UI Card berhasil digambar di FigCraft!")
            return True
    except Exception as e:
        print(f"[-] Gagal menjalankan demo: {e}")
        return False

