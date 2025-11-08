@echo off
echo BUILDING FLAWLESS BMI 2025...
rd /s /q build dist __pycache__ 2>nul
del *.spec 2>nul
pyinstaller --onefile --windowed --noconsole --name BMI2025 --add-data "bmi_core.py;." main.py
if exist "dist\BMI2025.exe" start "" dist\BMI2025.exe
echo DONE! Close me.
pause