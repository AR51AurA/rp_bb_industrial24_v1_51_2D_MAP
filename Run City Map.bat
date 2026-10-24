@echo off
title City 24i Map
cd /d "%~dp0"
where py >nul 2>nul && (py -3 citymap_server.py & goto end)
where python >nul 2>nul && (python citymap_server.py & goto end)
echo Python 3 was not found. Install it from https://www.python.org/downloads/ (tick "Add python.exe to PATH"),
echo or just open index.html in your browser instead.
:end
pause
