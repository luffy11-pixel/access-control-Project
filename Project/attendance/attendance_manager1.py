import csv
from datetime import datetime
from pathlib import Path
import json
from matcher import load_roster, match_student
from OCR.ocr_reader import ocr_extract_text  # make sure folder name is lowercase
from utils.file_utils import get_image_files


class AttendanceManager:
    def __init__(self, roster_file):
        self.roster = self.load_roster(roster_file)
        self.session_attendance = set()
        self.attendance_log = []

    def mark_attendance_folder(self, folder_path, threshold=150):
        """Mark attendance for all images in a folder without inserting duplicates."""
        image_files = get_image_files(folder_path)

        for file in image_files:
            result = self.mark_attendance_no_duplicate(file, threshold)
            print(result)

    def load_roster(self, file_path):
        return load_roster(file_path)

    def mark_attendance(self, image_path, threshold=150):
        ocr_text = ocr_extract_text(image_path, threshold)
        student = match_student(ocr_text, self.roster)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if student:
            student_id = student["id"]
            if student_id not in self.session_attendance:
                self.session_attendance.add(student_id)
                self.attendance_log.append(
                    {
                        "id": student_id,
                        "name": student["name"].title(),
                        "timestamp": timestamp,
                    }
                )
                return f"Attendance marked for {student['name'].title()} at {timestamp}"
            else:
                return f"Attendance already marked for {student['name'].title()}"
        else:
            return "Student not recognized"

    def save_attendance(self, output_file=None, filetype="csv"):
        # Automatic timestamped filename if not provided
        if output_file is None:
            output_file = (
                f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{filetype}"
            )

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        filepath = Path(output_file)
        if filetype.lower() == "csv":
            with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
                # Include 'status' field
                fieldnames = ["timestamp", "id", "name"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for record in self.attendance_log:
                    writer.writerow(record)

        elif filetype.lower() == "json":
            with open(filepath, mode="w", encoding="utf-8") as jsonfile:
                json.dump(self.attendance_log, jsonfile, ensure_ascii=False, indent=4)

        else:
            raise ValueError("Unsupported file type. Use 'csv' or 'json'.")

        return filepath
