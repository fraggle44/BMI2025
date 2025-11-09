# Dev Setup
```bash
pip install pyqt6 pyinstaller pytest-qt
pyinstaller --onefile --windowed --name BMI2025 --add-data "bmi_core.py;." main.py