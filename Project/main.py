# File: main.py

import sys
from attendance.attendance_manager import AttendanceManager


def main():
    print("=== OCR-Based Attendance System ===\n")

    # Load roster file
    roster_file = input("Enter path to roster file (CSV or JSON): ").strip()
    manager = AttendanceManager(roster_file)

    while True:
        print("\nSelect mode:")
        print("1. Single image")
        print("2. Batch folder")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            image_path = input("Enter path to student ID image: ").strip()
            result = manager.mark_attendance(image_path)
            print(result)

        elif choice == "2":
            folder_path = input("Enter folder path containing ID images: ").strip()
            manager.mark_attendance_folder(folder_path)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Try again.")

    # Export attendance
    print("\nExporting attendance records...")
    filetype = input("Enter export file type (csv/json): ").strip().lower()
    if filetype not in ["csv", "json"]:
        print("Invalid file type. Defaulting to CSV.")
        filetype = "csv"

    output_file = input(
        "Enter output file path (leave blank for auto timestamp): "
    ).strip()
    if output_file == "":
        output_file = None

    filepath = manager.save_attendance(output_file, filetype)
    print(f"Attendance saved to: {filepath}")

    print("\n✅ Done! Exiting program.")


if __name__ == "__main__":
    main()
