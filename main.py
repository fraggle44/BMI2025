# main.py — FINAL FIXED: Clipboard works + no crash
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
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(25, 25, -25, -25)
        grad = QConicalGradient(self.width()//2, self.height()//2, 90)
        grad.setColorAt(0, QColor("#00D4FF"))
        grad.setColorAt(0.5, QColor("#FFB800"))
        grad.setColorAt(1, QColor("#FF6B6B"))
        pen = p.pen()
        pen.setWidth(20)
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
        self.setFixedSize(480, 760)
        self.unit = "metric"
        self.load_config()
        self.setup_ui()

    def load_config(self):
        try:
            with open(CONFIG_FILE) as f:
                self.unit = json.load(f).get("unit", "metric")
        except: pass

    def save_config(self):
        CONFIG_FILE.write_text(json.dumps({"unit": self.unit}))

    def setup_ui(self):
        central = QWidget()
        central.setStyleSheet("background: #0a0a15;")
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.setSpacing(5)
        lay.setContentsMargins(50, 15, 50, 5)

        title = QLabel("BMI Calculator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font: bold 36pt 'Segoe UI'; color: #00D4FF;")
        lay.addWidget(title)

        lay.addSpacing(20)

        unit_lay = QHBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(["Metric (kg/cm)", "Imperial (lbs/in)"])
        self.combo.setCurrentIndex(0 if self.unit == "metric" else 1)
        self.combo.currentIndexChanged.connect(self.toggle_unit)
        self.combo.setStyleSheet("background: rgba(0,212,255,0.25); border-radius: 20px; padding: 12px; font: 18px; color: white;")
        unit_lay.addStretch()
        unit_lay.addWidget(self.combo)
        unit_lay.addStretch()
        lay.addLayout(unit_lay)

        lay.addSpacing(30)

        card = QFrame()
        card.setFixedSize(380, 180)
        card.setStyleSheet("""
            background: rgba(255,255,255,0.08);
            border: 2px solid #00D4FF;
            border-radius: 30px;
            backdrop-filter: blur(20px);
        """)
        card_lay = QVBoxLayout(card)
        card_lay.setSpacing(20)
        card_lay.setContentsMargins(25, 25, 25, 25)

        self.w_input = QLineEdit()
        self.h_input = QLineEdit()
        for w in (self.w_input, self.h_input):
            w.setFixedHeight(50)
            w.setStyleSheet("""
                background: rgba(10,10,30,0.85);
                border: 2px solid #00D4FF;
                border-radius: 20px;
                padding: 0px 20px;
                font: bold 20pt 'Consolas';
                color: #00D4FF;
            """)
            w.returnPressed.connect(self.calculate)
            w.textChanged.connect(self.on_text_changed)
        card_lay.addWidget(self.w_input)
        card_lay.addWidget(self.h_input)
        lay.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        lay.addSpacing(60)

        self.gauge = BMIGauge()
        lay.addWidget(self.gauge, alignment=Qt.AlignmentFlag.AlignCenter)

        self.result = QLabel("Enter values to see BMI")
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setStyleSheet("color: white; font: 12pt 'Segoe UI';")
        lay.addWidget(self.result)

        lay.addSpacing(15)

        lay.addStretch()
        btn_lay = QHBoxLayout()
        btn_lay.addStretch()
        calc = QPushButton("Calculate")
        self.copy_btn = QPushButton("Copy")  # ← DIRECT REFERENCE
        for b in (calc, self.copy_btn):
            b.setFixedHeight(60)
            b.setMinimumWidth(130)
            b.setStyleSheet("""
                background: #00D4FF; color: black; font: bold 18pt 'Segoe UI';
                border-radius: 30px;
            """)
        calc.clicked.connect(self.calculate)
        self.copy_btn.clicked.connect(self.copy_result)
        btn_lay.addWidget(calc)
        btn_lay.addSpacing(20)
        btn_lay.addWidget(self.copy_btn)
        btn_lay.addStretch()
        lay.addLayout(btn_lay)

        lay.addSpacing(10)

        self.update_units()
        QTimer.singleShot(100, self.w_input.setFocus)
        QTimer.singleShot(200, lambda: self.gauge.animate(0))

    def on_text_changed(self):
        for w in (self.w_input, self.h_input):
            color = "white" if w.text() else "#00D4FF"
            w.setStyleSheet(f"""
                background: rgba(10,10,30,0.85);
                border: 2px solid #00D4FF;
                border-radius: 20px;
                padding: 0px 20px;
                font: bold 20pt 'Consolas';
                color: {color};
            """)

    def toggle_unit(self, i):
        self.unit = "metric" if i == 0 else "imperial"
        self.save_config()
        self.update_units()
        self.calculate(silent=True)

    def update_units(self):
        m = self.unit == "metric"
        self.w_input.setPlaceholderText("Weight (kg)" if m else "Weight (lbs)")
        self.h_input.setPlaceholderText("Height (cm)" if m else "Height (in)")
        self.on_text_changed()

    def calculate(self, silent=False):
        try:
            w = float(self.w_input.text() or 0)
            h = float(self.h_input.text() or 0)
            if w <= 0 or h <= 0: raise ValueError
            kg = w if self.unit == "metric" else lbs_to_kg(w)
            cm = h if self.unit == "metric" else in_to_cm(h)
            r = calculate_bmi(kg, cm)
            self.gauge.animate(r.value)
            badge = f'<span style="background:{r.color};padding:10px 20px;border-radius:20px;color:#000;font-weight:900;font-size:27pt;">{r.category.name.title()}</span>'
            self.result.setText(
                f"<span style='font-size:27pt; font-weight: bold;'>{r.value}</span>"
                f"<div style='margin-top:5px;'>{badge}</div>"
                f"<div style='margin-top:8px;'><b style='font-size:8pt;'>{r.tip}</b></div>"
            )
            self.result.setProperty("data", f"BMI: {r.value}\nCategory: {r.category.name.title()}\nTip: {r.tip}")
        except:
            if not silent:
                QMessageBox.critical(self, "Error", "Please enter valid numbers.")

    def copy_result(self):
        txt = self.result.property("data") or ""
        QApplication.clipboard().setText(txt)
        
        # DIRECT REFERENCE — NO FINDCHILD
        original_style = self.copy_btn.styleSheet()
        
        self.copy_btn.setText("Copied! ✓")
        self.copy_btn.setStyleSheet("""
            background: #00ff88; color: black; font: bold 20pt 'Segoe UI';
            border-radius: 30px; box-shadow: 0 0 30px #00ff88;
        """)
        
        QTimer.singleShot(1500, lambda: [
            self.copy_btn.setText("Copy"),
            self.copy_btn.setStyleSheet(original_style)
        ])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())