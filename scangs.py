import requests
from bs4 import BeautifulSoup
from googlescholar import fetch_scholar_data
import urllib3
import time
from googlescholar import *
from scanauth import extract_degree_type
import csv
from linkedin import fetch_linkedin_url
from llm import gs_queries
import os

def search_google_scholar(query):
    
    search_url = f"https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={query}&btnG="
    #print(search_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    max_retries = 5
    for attempt in range(max_retries):
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            time.sleep(5)  
        else:
            raise Exception(f"Failed to fetch the webpage. Status code: {response.status_code}")
    else:
        raise Exception("Max retries exceeded. Could not fetch the webpage.")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    profiles = []
    for link in soup.select('.gs_ai_name a'):
        profiles.append("https://scholar.google.com" + link['href'])
    return profiles



            

import csv
import os

def write_profile_to_csv(profiles, filename="datalog/scholar.csv"):
    # Prepare to track seen URLs
    seen_urls = set()
    fieldnames = profiles[0].keys() if profiles else []

    # Check if file exists to determine if headers are needed
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Only write header if file didn't exist (first run)
        if not file_exists:
            writer.writeheader()

        for profile in profiles:
            scholar_url = profile.get('scholar_url', None)
            # Only write profile if URL has not been seen
            if scholar_url not in seen_urls:
                seen_urls.add(scholar_url)
                writer.writerow(profile)

    print(f"Data written to {filename} with duplicates based on scholar_url removed.")

    
    
def topk_googlescholar(k, location=None):
    
    profiles = []
    filtered_profiles = []
    for query in gs_queries:
        if location:
            query += f" {location}"
        #print(f"Searching for {query}")
        profiles += search_google_scholar(query)
        
        for profile in profiles:
            scholar_data = fetch_scholar_data(profile)
            degree_type = extract_degree_type(profile)
            if degree_type != "flagged":
                filtered_profiles.append({
                    'scholar_url': profile,
                    'name': scholar_data.get('name', 'N/A'),
                    'citations': scholar_data.get('citations', 'N/A'),
                    'h_index': scholar_data.get('h_index', 'N/A'),
                    'relevance_score': scholar_data.get('relevance_score',0),
                    'degree_type': degree_type,
                    'Linkedin': fetch_linkedin_url(scholar_data.get('name', 'N/A'),scholar_data.get('location', 'N/A'))
                })
                print(profile)
                
            time.sleep(1)  

    sorted_profiles = sorted(filtered_profiles, key=lambda x: x['relevance_score'], reverse=True)
    if not sorted_profiles:
        return []
    write_profile_to_csv(sorted_profiles)
    return sorted_profiles

if __name__ == "__main__":
    top_k_profiles = topk_googlescholar(12, "Seattle")
    #write_profile_to_csv(top_k_profiles)
    for profile in top_k_profiles:
        print(f"Name: {profile['name']}\n relevance: {profile['relevance_score']}\n citations: {profile['citations']}\n H-index: {profile['h_index']}\n Degree/Institute of Work: {profile['degree_type']}\n Profile Link: {profile['scholar_url']}\n Linkedin: {profile['Linkedin']}\n")
