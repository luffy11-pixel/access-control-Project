import json
import csv
from OCR.ocr_reader import ocr_extract_text
from difflib import SequenceMatcher


def load_roster(file_path):
    roster = []

    if file_path.endswith(".csv"):
        import csv

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                roster.append({"id": row["id"].strip(), "name": row["name"].strip()})
    elif file_path.endswith(".json"):
        import json

        with open(file_path, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            for row in data:
                roster.append({"id": row["id"].strip(), "name": row["name"].strip()})
    else:
        raise ValueError("Unsupported roster format. Use CSV or JSON")

    return roster


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def match_student(roster, image_path, threhold=150, threshold=0.6):
    extract_text = (
        ocr_extract_text(image_path, threhold)
        .lower()
        .replace("\n", " ")
        .strip()
    )
    for student in roster:
        # Make sure student is a dictionary
        if not isinstance(student, dict):
            continue

        if (
            student["name"].lower() in extract_text
            or student["id"].lower() in extract_text
        ):
            name_match = similar(extract_text, student["name"].lower())
            id_match = similar(extract_text, student["id"].lower())
            if name_match >= threshold or id_match >= threshold:
                return student

    return None
