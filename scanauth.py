import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
from authors import *
import urllib3
from prof import *
from linkedin import fetch_linkedin_url
import os
import csv

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
                if "professor" in degree_type.lower():
                    degree_type = "flagged"
                return degree_type
            return "Unknown 2"
        elif response.status == 429:
            attempt += 1
            wait_time = attempt
            print(f"Retry in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            return "Unknown 1"
    return "Unknown 3"

def get_degree_type(author_name, prof_name, university):
    query = f"{author_name} Google Scholar {university}"
    for url in search(query, num_results=5):
        if 'scholar.google.com/citations?' in url:
            return extract_degree_type(url), url
    return "Unknown", "None"

def filter_authors(authors_list):
    filtered_authors = []
    seen_urls = set()
    for author in authors_list:
        name, prof_name, university = author
        degree_type, url = get_degree_type(name, prof_name, university)
        linkedin_url = fetch_linkedin_url(name, degree_type)
        if url != "None" and url not in seen_urls:
            seen_urls.add(url)
            if degree_type != 'flagged':
                filtered_authors.append((name, url, linkedin_url, prof_name, university, degree_type, "ML"))
        time.sleep(1) 
    return filtered_authors

def write_authors_to_csv(authors, filename):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        if os.path.getsize(filename) == 0:
            csv_writer.writerow(['Name', 'scholar_url', 'Linkedin', 'professor/Lab-head', 'university', 'Degree/Institution', 'Field'])
        for author in authors:
            csv_writer.writerow(author)

def main():
    prof_name = input("Enter the professor's name: ")
    university = input("Enter the university: ")
    inprr = int(input("How many student: "))
    inpr = 3 * inprr
    prof_url = get_professor_url(prof_name, university)
    if not prof_url:
        print("Google Scholar URL not found.")
        return

    #print(f"Found Google Scholar URL: {prof_url}")
    citation_links = get_citation_links(prof_url)
    all_authors = []

    for link in citation_links:
        authors = get_authors_from_citation(link)
        for author in authors:
            all_authors.append((author, prof_name, university))
        time.sleep(0.5)  
    # for aut in all_authors:
    #     print(aut)
    all_authors = all_authors[:inpr]
    filtered_authors = filter_authors(all_authors)
    filtered_authors = filtered_authors[:inprr]
    
    print("Filtered authors with degree types:")
    for author in filtered_authors:
        print(author)
    write_authors_to_csv(filtered_authors, 'authors.csv')
    
def remain(university, k):
    inprr = k
    inpr = 3 * inprr
    profs = professors[university]
    all_authors = []
    for proff in profs:
        prof_name = proff['name']
        prof_url = get_professor_url(prof_name, university)
        if not prof_url:
            print("Google Scholar URL not found.")
            return

        #print(f"Found Google Scholar URL: {prof_url}")
        citation_links = get_citation_links(prof_url)
        for link in citation_links:
            authors = get_authors_from_citation(link)
            for author in authors:
                all_authors.append((author, prof_name, university))
            time.sleep(1)  
    # for aut in all_authors:
    #     print(aut)
    all_authors = all_authors[:inpr]
    filtered_authors = filter_authors(all_authors)
    #filtered_authors = filtered_authors[:inprr]
    
    print("Filtered authors with degree types:")
    for author in filtered_authors:
        print(author)
    write_authors_to_csv(filtered_authors, 'datalog/filtered_authors.csv')

if __name__ == "__main__":
    main()
