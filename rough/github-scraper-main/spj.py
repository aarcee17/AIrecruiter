import json

# Read the JSON file
with open('github_data.json', 'r') as file:
    data = json.load(file)

# Process the data
print(data)
