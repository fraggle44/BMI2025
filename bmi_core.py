from pydantic import BaseModel, PositiveFloat
from enum import Enum

class Category(Enum):
    UNDERWEIGHT = "underweight"
    NORMAL = "normal"
    OVERWEIGHT = "overweight"
    OBESE = "obese"

class BMIResult:
    def __init__(self, value, category, tip, color):
        self.value = value
        self.category = category
        self.tip = tip
        self.color = color

def calculate_bmi(weight_kg: float, height_cm: float) -> BMIResult:
    bmi = weight_kg / ((height_cm / 100) ** 2)
    bmi = round(bmi, 1)
    if bmi < 18.5:
        return BMIResult(bmi, Category.UNDERWEIGHT, "Consider nutrient-dense foods.", "#FFB800")
    elif bmi < 25:
        return BMIResult(bmi, Category.NORMAL, "Great job maintaining a healthy weight!", "#00D4FF")
    elif bmi < 30:
        return BMIResult(bmi, Category.OVERWEIGHT, "Small lifestyle tweaks can help.", "#FF6B6B")
    else:
        return BMIResult(bmi, Category.OBESE, "Consult a professional for support.", "#C92C2C")

def kg_to_lbs(kg): return round(kg * 2.20462, 2)
def lbs_to_kg(lbs): return round(lbs / 2.20462, 2)
def cm_to_in(cm): return round(cm / 2.54, 1)
def in_to_cm(inch): return round(inch * 2.54, 1)