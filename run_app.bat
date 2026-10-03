@echo off
echo ========================================================
echo   AETHERCRYPT WORKBENCH - SISTEM SANDI KLASIK MULTI-LAPIS
echo   Kriptografi (IF21A05) - Universitas Jenderal Soedirman
echo ========================================================
echo.
echo [*] Membuka Backend FastAPI pada http://127.0.0.1:8000
start "AetherCrypt Backend (FastAPI)" cmd /k "%~dp0start_backend.bat"

timeout /t 2 /nobreak >nul

echo [*] Membuka Frontend React pada http://localhost:5173
start "AetherCrypt Frontend (Vite)" cmd /k "%~dp0start_frontend.bat"

timeout /t 2 /nobreak >nul

echo.
echo [OK] Seluruh server telah berjalan!
echo Buka browser pada: http://localhost:5173
echo.
pause
