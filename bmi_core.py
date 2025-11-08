# bmi_core.py  ←  PASTE THIS ENTIRE BLOCK (replace top 12 lines)
from __future__ import annotations
from dataclasses import dataclass
from pydantic import BaseModel, PositiveFloat
from enum import Enum

class Category(Enum):
    UNDERWEIGHT = "underweight"
    NORMAL = "normal"
    OVERWEIGHT = "overweight"
    OBESE = "obese"

@dataclass(frozen=True)
class BMIResult:
    value: float
    category: Category
    tip: str
    color: str

class BMIInput(BaseModel):
    weight_kg: PositiveFloat
    height_cm: PositiveFloat

def calculate_bmi(weight_kg: float, height_cm: float) -> BMIResult:
    bmi = weight_kg / ((height_cm / 100) ** 2)
    bmi = round(bmi, 1)

    if bmi < 18.5:
        cat, color, tip = Category.UNDERWEIGHT, "#FFB800", "Consider nutrient-dense foods."
    elif bmi < 25:
        cat, color, tip = Category.NORMAL, "#00D4FF", "Great job maintaining a healthy weight!"
    elif bmi < 30:
        cat, color, tip = Category.OVERWEIGHT, "#FF6B6B", "Small lifestyle tweaks can help."
    else:
        cat, color, tip = Category.OBESE, "#C92C2C", "Consult a professional for support."

    return BMIResult(bmi, cat, tip, color)

# Unit converters
def kg_to_lbs(kg: float) -> float: return round(kg * 2.20462, 2)
def lbs_to_kg(lbs: float) -> float: return round(lbs / 2.20462, 2)
def cm_to_in(cm: float) -> float: return round(cm / 2.54, 1)
def in_to_cm(inch: float) -> float: return round(inch * 2.54, 1)