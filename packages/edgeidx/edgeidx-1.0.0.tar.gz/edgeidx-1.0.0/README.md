# edgeIDX

## Overview
edgeIDX is a Python package for extracting Aadhaar card details (Name, DOB, Gender, and Aadhaar Number) from images using Tesseract OCR. Unlike traditional setups, this package embeds a trained Tesseract model within itself, eliminating the need for a separate `tesseract.exe` installation.

## Features
- Extracts Aadhaar card details using OCR.
- Uses an embedded Tesseract model, requiring no external dependencies.
- Supports image preprocessing to improve OCR accuracy.
- Works across different platforms without requiring external Tesseract installation.
- Can be integrated with Android applications for automated Aadhaar data extraction.

## System Requirements
- Python 3.7+
- OpenCV for image processing
- NumPy for handling image arrays
- Pytesseract for OCR

## Installation

### 1. Install via pip (After Publishing on PyPI)
```sh
pip install edgeidx


