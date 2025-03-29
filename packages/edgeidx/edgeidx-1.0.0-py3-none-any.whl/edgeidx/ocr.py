import pytesseract
import re
import json
import os
from .utils import preprocess_image, get_tessdata_prefix

# Set up Tesseract to use the embedded traineddata file
tessdata_dir = get_tessdata_prefix()
os.environ["TESSDATA_PREFIX"] = tessdata_dir

def extract_text_from_image(image):
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(image, config=custom_config)

def extract_data_from_image(image):
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)

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
    processed_img = preprocess_image(image_path)
    extracted_text = extract_text_from_image(processed_img)
    extracted_data = extract_data_from_image(processed_img)
    extracted_details = extract_all_details(extracted_text, extracted_data)
    return json.dumps(extracted_details, indent=4)
