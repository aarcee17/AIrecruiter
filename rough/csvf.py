import csv

def write_dict_to_csv(data, filename):
    if not data:
        print("No data to write.")
        return

    keys = set()
    for entry in data:
        keys.update(entry.keys())

    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Example usage
data = [
    {"name": "Raj", "age": 13, "birth": "2007-09-01"},
    {"name": "Sheet", "class": 10, "income": 13}
]

write_dict_to_csv(data, 'output.csv')
