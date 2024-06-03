import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import csv

def get_scholar_url(name, university):
    query = f"{name} Google Scholar {university}"
    for url in search(query, num_results=5):
        if 'scholar.google.com/citations?' in url:
            return url
    return None

def search_github_username(name, university):
    query = f"{name} {university} GitHub"
    for url in search(query, num_results=5):
        if 'github.com' in url:
            return url.split('/')[-1]
    return None

def extract_student_details(student):
    name, prof, university, degree_type, field_of_study = student
    github_username = search_github_username(name, university)
    scholar_url = get_scholar_url(name, university)
    return {
        "name": name,
        "professor": prof,
        "university": university,
        "degree_type": degree_type,
        "field_of_study": field_of_study,
        "github_username": github_username,
        "scholar_url": scholar_url
    }

def main():
    # Read from CSV
    students = []
    with open('filtered_authors.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append((row['name'], row['professor'], row['university'], row['degree_type'], row['field_of_study']))
    
    student_details = []
    for student in students:
        details = extract_student_details(student)
        student_details.append(details)
        time.sleep(1)  # Respect rate limits

    # Print or save the details
    for detail in student_details:
        print(detail)

if __name__ == "__main__":
    main()
