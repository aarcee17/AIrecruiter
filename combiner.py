import csv
import os

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def merge_csv_files(github_file, authors_file, scholars_file, output_file):
    github_data = read_csv(github_file)
    authors_data = read_csv(authors_file)
    scholars_data = read_csv(scholars_file)

    merged_data = github_data + authors_data + scholars_data

    all_keys = set()
    for data in merged_data:
        all_keys.update(data.keys())

    preferred_order = ['name', 'linkedin', 'scholar_url', 'github']

    # Filter out NoneType and sort remaining keys alphabetically
    sorted_keys = sorted(key for key in all_keys if key not in preferred_order and key is not None)

    # Add preferred order keys at the beginning
    sorted_keys = preferred_order + sorted_keys

    # Fill missing fields with blanks
    for data in merged_data:
        for key in sorted_keys:
            if key not in data:
                data[key] = ''

    write_csv(output_file, merged_data, sorted_keys)

if __name__ == "__main__":
    github_file = 'datalog/github_profiles.csv'  # Replace with your actual file path
    authors_file = 'datalog/filtered_authors.csv'  # Replace with your actual file path
    scholars_file = 'datalog/scholar.csv'  # Replace with your actual file path
    output_file = 'datalog/merged_output.csv'  # Replace with your desired output file path
    
    merge_csv_files(github_file, authors_file, scholars_file, output_file)
    print(f"Merged CSV files written to {output_file}")
