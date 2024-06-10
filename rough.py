import csv
def remove_duplicates(input_csv, output_csv):
    unique_profiles = {}
    
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            scholar_url = row['scholar_url']
            if scholar_url not in unique_profiles:
                unique_profiles[scholar_url] = row
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = unique_profiles[next(iter(unique_profiles))].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for profile in unique_profiles.values():
            writer.writerow(profile)
            
remove_duplicates('scholars.csv','scholar.csv')            