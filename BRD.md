# BMI Calculator Desktop App – Business Requirements Document (BRD)

**Version:** 1.0 | **Status:** LOCKED  
**Product Owner:** SuperGrok Heavy PO  
**Date:** 08 Nov 2025  

## 1. Vision
A 2025-modern, single-command desktop BMI calculator that feels like a native macOS/Windows app with zero install friction.

## 2. Core Features
1. **Dual Unit System**  
   - Metric (kg / cm)  
   - Imperial (lbs / inches)  
   - One-click toggle with live conversion  
2. **Live Input Validation**  
   - Real-time numeric-only enforcement  
   - Visual error toast on invalid entry  
3. **BMI Result Panel**  
   - BMI value to 1 decimal  
   - WHO category badge (color-coded)  
   - One-sentence health tip  
   - “Copy to Clipboard” micro-interaction  
4. **Persistence**  
   - Last unit system saved to `%APPDATA%/bmi_calc/config.json`  
5. **Modern UI**  
   - Dark glassmorphism card  
   - Neon cyan accent (#00D4FF)  
   - Animated BMI gauge ring (0→value in 800ms)  
   - Enter-key submit  
   - Light/Dark auto-toggle via OS theme  

## 3. Non-Functional
- Python 3.12, PyQt6, PyInstaller --onefile  
- 100 % unit test coverage, 95 % UI coverage  
- Launch via `run.bat` (Win) / `run.sh` (macOS/Linux)  
- MkDocs documentation site  

## 4. Acceptance Criteria
- [x] One-click launch opens native window  
- [x] All 25 pytest cases pass  
- [x] SHA256 checksum matches  
- [x] Figma mock embedded in README  

**LOCKED. No changes permitted.**