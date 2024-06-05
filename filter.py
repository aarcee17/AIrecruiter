import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
from authors import get_professor_url, get_citation_links, get_authors_from_citation
import urllib3
import requests
from bs4 import BeautifulSoup
import time
from prof import *
def extract_degree_type(scholar_url, retries=5):
    http = urllib3.PoolManager()
    attempt = 0
    while attempt < retries:
        response = http.request('GET', scholar_url)
        if response.status == 200:
            soup = BeautifulSoup(response.data, 'html.parser')
            designation_element = soup.find('div', class_='gsc_prf_il')
            if designation_element:
                degree_type = designation_element.text.strip()
                #print(degree_type)
                if "professor" in degree_type.lower():
                    degree_type = "flagged"
                return degree_type
            return "Unknown 2"
        elif response.status == 429:
            attempt += 1
            wait_time = 1.5 ** attempt
            print(f"retry in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            return "Unknown 1"
    return "Unknown 3"


def get_degree_type(author_name, prof_name, university):
    query = f"{author_name} Google Scholar {university}"
    for url in search(query, num_results=5):
        if 'scholar.google.com/citations?' in url:
            #print("url is "+ url)
            return extract_degree_type(url), url
    return "res 1", "None"



def filter_authors(authors_list):
    filtered_authors = []
    for author in authors_list:
        name, prof_name, university = author
        degree_type, url = get_degree_type(name, prof_name, university)
        if (degree_type != 'flagged'):
            filtered_authors.append((name,url, prof_name, university, degree_type, "ML"))
        time.sleep(1) 
    return filtered_authors

import csv

def write_authors_to_csv(authors, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['name','url', 'professor', 'university', 'degree_type', 'field_of_study'])
        for author in authors:
            csv_writer.writerow(author)


def main():
    prof_name = input("Enter the professor's name: ")
    university = input("Enter the university: ")
    inprr = int(input("How many student: "))
    inpr = 3*inprr
    prof_url = get_professor_url(prof_name, university)
    if not prof_url:
        print("Google Scholar URL not found.")
        return

    print(f"Found Google Scholar URL: {prof_url}")
    citation_links = get_citation_links(prof_url)
    all_authors = []

    for link in citation_links:
        authors = get_authors_from_citation(link)
        for author in authors:
            all_authors.append((author, prof_name, university))
        time.sleep(1)  
    for aut in all_authors:
        print(aut)
    all_authors = all_authors[:inpr]
    filtered_authors = filter_authors(all_authors)
    #score_filtered_authors = score_authors(filtered_authors)
    #print("Filtered authors with scores:")
    filtered_authors = filtered_authors[:inprr]
    
    
    print("Filtered authors with degree types:")
    for author in filtered_authors:
        print(author)
    write_authors_to_csv(filtered_authors, 'filtered_authors.csv')
    
    
def remain(university,k):
    
    university = university
    inprr = k
    inpr = 3*inprr
    profs = professors[university]
    all_authors = []
    for proff in profs:
        prof_name = proff['name']
        prof_url = get_professor_url(prof_name, university)
        if not prof_url:
            print("Google Scholar URL not found.")
            return

        print(f"Found Google Scholar URL: {prof_url}")
        citation_links = get_citation_links(prof_url)
        

        for link in citation_links:
            authors = get_authors_from_citation(link)
            for author in authors:
                all_authors.append((author, prof_name, university))
            time.sleep(1)  
    for aut in all_authors:
        print(aut)
    all_authors = all_authors[:inpr]
    filtered_authors = filter_authors(all_authors)
    #score_filtered_authors = score_authors(filtered_authors)
    #print("Filtered authors with scores:")
    filtered_authors = filtered_authors[:inprr]
    
    
    print("Filtered authors with degree types:")
    for author in filtered_authors:
        print(author)
    write_authors_to_csv(filtered_authors, 'filtered_authors.csv')

# def main():
#     print(get_degree_type('Michael I Jordan', 'Andrew NG', 'Stanford University'))
#     #print(extract_degree_type('https://scholar.google.com/citations?user=yxUduqMAAAAJ&hl=en'))
if __name__ == "__main__":
     main()    
     #remain('Stanford University',4)