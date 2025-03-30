import pytesseract
import re
import json
import os
import sys
from pathlib import Path
from .utils import preprocess_image

class TesseractEmbedder:
    @staticmethod
    def initialize():
        try:
            base_path = Path(__file__).parent.parent
            print(base_path)
            tess_bin = base_path / 'tesseract' / 'tesseract.exe'
            print(tess_bin)
            tessdata_path = base_path / 'tessdata'
            print(tessdata_path)

            if not tess_bin.exists():
                raise FileNotFoundError(f"Tesseract binary not found at {tess_bin}")
            if not tessdata_path.exists():
                raise FileNotFoundError(f"Tessdata directory not found at {tessdata_path}")

            # Debugging prints
            print(f"Tesseract Binary Path: {tess_bin}")
            print(f"Tessdata Path: {tessdata_path}")

            # Set environment variables
            os.environ["PATH"] = str(tess_bin.parent) + os.pathsep + os.environ["PATH"]
            os.environ["TESSDATA_PREFIX"] = str(tessdata_path)
            pytesseract.pytesseract.tesseract_cmd = str(tess_bin)

            # Debugging prints
            print(f"Updated PATH: {os.environ['PATH']}")
            print(f"Updated TESSDATA_PREFIX: {os.environ['TESSDATA_PREFIX']}")
            print(f"pytesseract.tesseract_cmd: {pytesseract.pytesseract.tesseract_cmd}")

            # Verify Tesseract can run
            try:
                version = pytesseract.get_tesseract_version()
                print(f"Tesseract version: {version}")
            except Exception as e:
                raise RuntimeError(f"Tesseract test failed: {str(e)}")

        except Exception as e:
            raise RuntimeError(f"Tesseract init failed: {str(e)}")

# [Rest of your existing functions]

def extract_text_from_image(image):
    """Extract text from image using embedded Tesseract"""
    try:
        custom_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(image, config=custom_config)
    except pytesseract.TesseractError as e:
        raise RuntimeError(f"OCR processing failed: {str(e)}")

def extract_data_from_image(image):
    """Extract OCR data from image using embedded Tesseract"""
    try:
        custom_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_data(
            image, 
            config=custom_config, 
            output_type=pytesseract.Output.DICT
        )
    except pytesseract.TesseractError as e:
        raise RuntimeError(f"OCR data extraction failed: {str(e)}")

def extract_name(text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        dob_match = re.search(r'\d{2}/\d{2}/\d{4}', line)
        if dob_match and i > 0:
            name_line = lines[i - 1].strip()
            name_words = re.sub(r'[^A-Za-z ]+', '', name_line).strip().split()
            return ' '.join(name_words[-3:])
    return ""

def extract_dob(text):
    match = re.search(r'\d{2}/\d{2}/\d{4}', text)
    return match.group(0) if match else ""

def extract_gender(text, lines, dob_index):
    if dob_index < len(lines) - 1:
        next_lines = [re.sub(r'[^A-Za-z ]+', '', lines[j].strip()) for j in range(dob_index + 1, min(dob_index + 6, len(lines)))]
        next_text = " ".join(next_lines).lower()

        if re.search(r'\b(male|m)\b', next_text):
            return "Male"
        elif re.search(r'\b(female|f)\b', next_text):
            return "Female"
    return ""

def extract_aadhaar_number(data):
    aadhaar_number_parts = []
    four_digit_pattern = r'\d{4}'
    eight_digit_pattern = r'\d{8}'
    twelve_digit_pattern = r'\d{12}'

    for word in data.get('text', []):
        word = word.strip()
        if re.fullmatch(four_digit_pattern, word):
            aadhaar_number_parts.append(word)
            if len(aadhaar_number_parts) == 3:
                break
        elif re.fullmatch(eight_digit_pattern, word):
            aadhaar_number_parts.append(word)
            if len(aadhaar_number_parts) == 2:
                break
        elif re.fullmatch(twelve_digit_pattern, word):
            aadhaar_number_parts.append(word)
            break

    if len(aadhaar_number_parts) == 3:
        return " ".join(aadhaar_number_parts)
    elif len(aadhaar_number_parts) == 2:
        combined = aadhaar_number_parts[0] + aadhaar_number_parts[1]
        if len(combined) == 12:
            return f"{combined[:4]} {combined[4:8]} {combined[8:]}"
    elif len(aadhaar_number_parts) == 1 and len(aadhaar_number_parts[0]) == 12:
        return f"{aadhaar_number_parts[0][:4]} {aadhaar_number_parts[0][4:8]} {aadhaar_number_parts[0][8:]}"
    return ""

def extract_all_details(text, data):
    lines = text.split("\n")
    dob = extract_dob(text)
    dob_index = next((i for i, line in enumerate(lines) if dob in line), -1)
    return {
        "Name": extract_name(text),
        "DOB": dob,
        "Gender": extract_gender(text, lines, dob_index),
        "Aadhaar Number": extract_aadhaar_number(data)
    }

def extract_aadhaar_details(image_path):
    """Main function to extract Aadhaar details from image"""
    try:
        processed_img = preprocess_image(image_path)
        extracted_text = extract_text_from_image(processed_img)
        extracted_data = extract_data_from_image(processed_img)
        extracted_details = extract_all_details(extracted_text, extracted_data)
        return json.dumps(extracted_details, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)
