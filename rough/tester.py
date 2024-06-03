import csv

def write_authors_to_csv(authors, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['name', 'professor', 'university', 'degree_type', 'field_of_study'])
        for author in authors:
            csv_writer.writerow(author)

# Example usage with data from filter.py
if __name__ == "__main__":
    authors = [
        ('Jason Chuang', 'Andrew NG', 'Stanford University', 'PhD', 'ML'),
        ('Christopher D Manning', 'Andrew NG', 'Stanford University', 'PhD', 'ML'),
        ('Andrew Y Ng', 'Andrew NG', 'Stanford University', 'PhD', 'ML'),
        ('Christopher Potts', 'Andrew NG', 'Stanford University', 'PostDoc', 'ML'),
        ('Yuval Netzer', 'Andrew NG', 'Stanford University', 'PhD', 'ML'),
        # Add more authors as needed...
    ]
    write_authors_to_csv(authors, 'filtered_authors.csv')
