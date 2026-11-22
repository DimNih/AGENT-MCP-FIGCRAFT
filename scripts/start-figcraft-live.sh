#!/usr/bin/env bash
# Bash Launcher for FigCraft Live Remote Mode (macOS / Linux)

set -e

echo "========================================================"
echo "  Starting FigCraft in Live Remote Control Mode (Port 9001)"
echo "========================================================"

find_figcraft() {
    if [ -n "$FIGCRAFT_PATH" ] && [ -f "$FIGCRAFT_PATH" ]; then
        echo "$FIGCRAFT_PATH"
        return
    fi

    # macOS candidates
    if [ "$(uname)" == "Darwin" ]; then
        for path in \
            "/Applications/FigCraft.app/Contents/MacOS/figcraft" \
            "$HOME/Applications/FigCraft.app/Contents/MacOS/figcraft" \
            "/usr/local/bin/figcraft" \
            "/opt/homebrew/bin/figcraft"; do
            if [ -f "$path" ]; then
                echo "$path"
                return
            fi
        done
    else
        # Linux candidates
        for path in \
            "/usr/bin/figcraft" \
            "/usr/local/bin/figcraft" \
            "$HOME/.local/bin/figcraft"; do
            if [ -f "$path" ]; then
                echo "$path"
                return
            fi
        done
    fi

    if command -v figcraft >/dev/null 2>&1; then
        command -v figcraft
        return
    fi

    return 1
}

BIN=$(find_figcraft || true)

if [ -z "$BIN" ]; then
    echo "[!] FigCraft binary not found!"
    echo "Please set FIGCRAFT_PATH environment variable."
    echo "Example: export FIGCRAFT_PATH=/path/to/figcraft"
    exit 1
fi

echo "[*] Launching: $BIN --control 9001"
"$BIN" --control 9001 &
echo "[✓] FigCraft started on port 9001. Happy designing!"

