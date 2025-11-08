# main.py — 100% CLEAN, NO TABS, PERFECT INDENTS
import PyQt6.sip
import sys, json, os
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtProperty
from PyQt6.QtGui import QPainter, QConicalGradient, QColor
from bmi_core import calculate_bmi, kg_to_lbs, lbs_to_kg, cm_to_in, in_to_cm

CONFIG_DIR = Path(os.getenv("APPDATA") or Path.home() / ".config", "bmi_calc")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"

class BMIGauge(QWidget):
    def __init__(self):
        super().__init__()
        self._value = 0
        self.setFixedSize(180, 180)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(20, 20, -20, -20)
        grad = QConicalGradient(self.width()//2, self.height()//2, 90)
        grad.setColorAt(0, QColor("#00D4FF"))
        grad.setColorAt(0.5, QColor("#FFB800"))
        grad.setColorAt(1, QColor("#FF6B6B"))
        pen = p.pen()
        pen.setWidth(16)
        pen.setBrush(grad)
        p.setPen(pen)
        p.drawArc(r, 225*16, -270*16 * (self._value / 50))

    def animate(self, target: float):
        self.anim = QPropertyAnimation(self, b"value", self)
        self.anim.setDuration(800)
        self.anim.setStartValue(self._value)
        self.anim.setEndValue(min(target, 50))
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    value = pyqtProperty(float,
        lambda self: self._value,
        lambda self, v: setattr(self, "_value", v) or self.update()
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator 2025")
        self.setFixedSize(420, 640)
        self.unit = "metric"
        self.load_config()
        self.setup_ui()

    def load_config(self):
        try:
            with open(CONFIG_FILE) as f:
                self.unit = json.load(f).get("unit", "metric")
        except:
            pass

    def save_config(self):
        CONFIG_FILE.write_text(json.dumps({"unit": self.unit}))

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.setSpacing(20)
        lay.setContentsMargins(30, 30, 30, 30)

        title = QLabel("BMI Calculator")
        title.setObjectName("title")
        lay.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        unit_lay = QHBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(["Metric (kg/cm)", "Imperial (lbs/in)"])
        self.combo.setCurrentIndex(0 if self.unit == "metric" else 1)
        self.combo.currentIndexChanged.connect(self.toggle_unit)
        unit_lay.addStretch()
        unit_lay.addWidget(self.combo)
        unit_lay.addStretch()
        lay.addLayout(unit_lay)

        card = QFrame()
        card.setObjectName("card")
        card_lay = QVBoxLayout(card)
        self.w_input = QLineEdit()
        self.w_input.setObjectName("input")
        self.h_input = QLineEdit()
        self.h_input.setObjectName("input")
        for w in (self.w_input, self.h_input):
            w.returnPressed.connect(self.calculate)
        card_lay.addWidget(self.w_input)
        card_lay.addWidget(self.h_input)
        lay.addWidget(card)

        self.gauge = BMIGauge()
        lay.addWidget(self.gauge, alignment=Qt.AlignmentFlag.AlignCenter)

        self.result = QLabel("Enter values to see BMI")
        self.result.setObjectName("result")
        lay.addWidget(self.result, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_lay = QHBoxLayout()
        calc = QPushButton("Calculate")
        calc.clicked.connect(self.calculate)
        copy = QPushButton("Copy")
        copy.clicked.connect(self.copy_result)
        for b in (calc, copy):
            b.setObjectName("btn")
        btn_lay.addWidget(calc)
        btn_lay.addWidget(copy)
        lay.addLayout(btn_lay)

        self.update_units()
        QTimer.singleShot(100, self.w_input.setFocus)

    def toggle_unit(self, i):
        self.unit = "metric" if i == 0 else "imperial"
        self.save_config()
        self.update_units()
        self.calculate(silent=True)

    def update_units(self):
        m = self.unit == "metric"
        self.w_input.setPlaceholderText("Weight (kg)" if m else "Weight (lbs)")
        self.h_input.setPlaceholderText("Height (cm)" if m else "Height (in)")

    def calculate(self, silent=False):
        try:
            w = float(self.w_input.text() or 0)
            h = float(self.h_input.text() or 0)
            if w <= 0 or h <= 0:
                raise ValueError
            kg = w if self.unit == "metric" else lbs_to_kg(w)
            cm = h if self.unit == "metric" else in_to_cm(h)
            r = calculate_bmi(kg, cm)
            self.gauge.animate(r.value)
            badge = f'<span style="background:{r.color};padding:6px 14px;border-radius:12px;color:#000;font-weight:900;">{r.category.name.title()}</span>'
            self.result.setText(f"<h2>{r.value}</h2><p>{badge}<br><b>{r.tip}</b></p>")
            self.result.setProperty("data", f"BMI: {r.value}\nCategory: {r.category.name.title()}\nTip: {r.tip}")
        except:
            if not silent:
                QMessageBox.critical(self, "Error", "Please enter valid numbers.")

    def copy_result(self):
        txt = self.result.property("data") or ""
        QApplication.clipboard().setText(txt)
        copy_btn = self.findChild(QPushButton, "Copy")
        copy_btn.setText("Copied!")
        QTimer.singleShot(1200, lambda: copy_btn.setText("Copy"))

STYLES = """
QMainWindow { background: #0a0a15; }
#title { color: #00D4FF; font: 700 36px "Segoe UI"; margin: 10px; }
#card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 24px;
    padding: 12px;
    backdrop-filter: blur(16px);
}
#input {
    background: rgba(0,0,0,0.35);
    border: 2px solid rgba(0,212,255,0.4);
    border-radius: 16px;
    padding: 12px 16px;     /* ← REDUCED VERTICAL PADDING */
    font: 900 23px "Consolas";
    color: white;
    min-height: 44px;       /* ← LOCKS HEIGHT */
}
#input:focus {
    border-color: #00D4FF;
    box-shadow: 0 0 20px #00D4FF;
}
#btn {
    background: #00D4FF;
    color: black;
    font: 700 16px "Segoe UI";
    border-radius: 16px;
    padding: 14px;
    min-width: 110px;
}
#btn:hover { background: #00f0ff; }
#result { color: white; font: 18px "Segoe UI"; text-align: center; }
QComboBox {
    background: rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 10px;
    color: white;
    font: 16px;
}
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLES)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())