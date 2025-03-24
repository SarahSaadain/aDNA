import os
import csv
import argparse

def load_replacements(csv_file: str):
    """Load old and new name pairs from the CSV file."""
    replacements = {}
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                old_name, new_name = row
                replacements[old_name] = new_name
    return replacements

def rename_files(folder: str, replacements: str, test_mode: bool):
    """Rename files in the given folder based on the replacements dictionary."""
    for filename in os.listdir(folder):
        new_filename = filename
        for old, new in replacements.items():
            if old in filename:
                new_filename = filename.replace(old, new)
                break  # Stop after first match

        if filename != new_filename:
            print(f"Renaming: {filename} -> {new_filename}")
            if not test_mode:
                os.rename(os.path.join(folder, filename), os.path.join(folder, new_filename))
        else:
            print(f"No change: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Rename files based on a CSV list.")
    parser.add_argument("csv_file", help="Path to the CSV file with old and new names")
    parser.add_argument("folder", help="Path to the folder containing files")
    parser.add_argument("--test", action="store_true", help="Enable test mode (no actual renaming)")

    args = parser.parse_args()
    replacements = load_replacements(args.csv_file)
    rename_files(args.folder, replacements, args.test)

if __name__ == "__main__":
    main()
