@echo off
setlocal enabledelayedexpansion
title FigCraft Live Remote Launcher

echo ========================================================
echo   Starting FigCraft in Live Remote Control Mode (Port 9001)
echo ========================================================
echo.

:: 1. Cek environment variable FIGCRAFT_PATH
if defined FIGCRAFT_PATH (
    if exist "%FIGCRAFT_PATH%" (
        set "FIGCRAFT_BIN=%FIGCRAFT_PATH%"
        goto :launch
    )
)

:: 2. Cek lokasi default Windows
if exist "%ProgramFiles%\ArtCraft\FigCraft\figcraft.exe" (
    set "FIGCRAFT_BIN=%ProgramFiles%\ArtCraft\FigCraft\figcraft.exe"
    goto :launch
)

if exist "%ProgramFiles(x86)%\ArtCraft\FigCraft\figcraft.exe" (
    set "FIGCRAFT_BIN=%ProgramFiles(x86)%\ArtCraft\FigCraft\figcraft.exe"
    goto :launch
)

if exist "%LocalAppData%\Programs\FigCraft\figcraft.exe" (
    set "FIGCRAFT_BIN=%LocalAppData%\Programs\FigCraft\figcraft.exe"
    goto :launch
)

:: 3. Cek di PATH
where figcraft.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "FIGCRAFT_BIN=figcraft.exe"
    goto :launch
)

echo [ERROR] Eksekutabel FigCraft tidak ditemukan!
echo Harap pasang FigCraft atau atur variabel lingkungan FIGCRAFT_PATH.
echo Contoh: set FIGCRAFT_PATH=C:\CustomPath\figcraft.exe
pause
exit /b 1

:launch
echo Menggunakan: "%FIGCRAFT_BIN%"
start "" "%FIGCRAFT_BIN%" --control 9001
echo.
echo [OK] FigCraft berhasil dibuka di port 9001!
echo Letakkan jendela FigCraft berdampingan dengan AI Agent Anda (Split Screen).
echo.
timeout /t 3 >nul
exit /b 0
