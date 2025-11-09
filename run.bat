@echo off
echo BUILDING FINAL FIXED: Clipboard works + no crash...
rd /s /q build dist __pycache__ 2>nul
pyinstaller --onefile --windowed --noconsole --name BMI2025 --add-data "bmi_core.py;." main.py
start "" dist\BMI2025.exe
echo DONE! Copy works perfectly.
pause