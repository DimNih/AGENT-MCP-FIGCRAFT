# PowerShell Launcher for FigCraft Live Remote Mode
$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting FigCraft in Live Remote Control Mode (Port 9001)" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

function Find-FigCraft {
    if ($env:FIGCRAFT_PATH -and (Test-Path $env:FIGCRAFT_PATH)) {
        return $env:FIGCRAFT_PATH
    }

    $candidates = @(
        "$env:ProgramFiles\ArtCraft\FigCraft\figcraft.exe",
        "${env:ProgramFiles(x86)}\ArtCraft\FigCraft\figcraft.exe",
        "$env:LocalAppData\Programs\FigCraft\figcraft.exe",
        "$HOME\.figcraft\bin\figcraft.exe"
    )

    foreach ($path in $candidates) {
        if (Test-Path $path) {
            return $path
        }
    }

    $cmd = Get-Command "figcraft.exe" -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    return $null
}

$bin = Find-FigCraft

if (-not $bin) {
    Write-Host "[!] FigCraft tidak ditemukan!" -ForegroundColor Red
    Write-Host "Silakan atur path via environment variable: `$env:FIGCRAFT_PATH = 'C:\Path\To\figcraft.exe'" -ForegroundColor Yellow
    Exit 1
}

Write-Host "[*] Membuka FigCraft dari: $bin" -ForegroundColor Gray
Start-Process -FilePath $bin -ArgumentList @("--control", "9001")
Write-Host "[✓] FigCraft berhasil dijalankan di port remote 9001!" -ForegroundColor Green
Write-Host "Buka jendela FigCraft ini berdampingan dengan Antigravity / AI Agent Anda." -ForegroundColor Cyan
