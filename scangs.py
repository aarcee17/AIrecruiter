import requests
from bs4 import BeautifulSoup
from googlescholar import fetch_scholar_data
import urllib3
import time
from googlescholar import *
from filter import extract_degree_type
import csv
from linkedin import fetch_linkedin_url
def top_labs(location):
    stack = []
    #we now need to pass or make  dtabase to retrievev a list of top labs. 
    # a good wuery would be Amazon Ml, apple Ml, google ML, mirosoft ML, openai Ml, etc....
    queries = [
        f"top AI labs {location}",
        f"best AI research labs {location}",
        f"leading AI research institutes {location}",
        f"prominent AI labs {location}",
        f"top machine learning labs {location}",
        f"best machine learning research labs {location}",
        f"leading machine learning research institutes {location}",
        f"prominent machine learning labs {location}"
    ]
    return stack
    
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


def write_profile_to_csv(profiles, filename="scholars.csv"):


  with open(filename, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=profiles[0].keys())
 
    if csvfile.tell() == 0:
      writer.writeheader()

    for profile in profiles:
        #profile.append('linkedin' :"fetch_linkedin_url(profile['name'],profile['location'])")
        writer.writerow(profile)
      

    
def topk_googlescholar(k, location=None):
    queries = ["Artifical Intelligence","Machine Learning"]
    #queries = ["AI Architect", "AI Architect"]
    #queries = top_labs(location=None)
    filtered_profiles = []
    for query in queries:
        if location:
            query += f" {location}"
        print(f"Searching for {query}")
        profiles = search_google_scholar(query)
        

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
            time.sleep(1)  
#n
    sorted_profiles = sorted(filtered_profiles, key=lambda x: x['relevance_score'], reverse=True)
    
    return sorted_profiles[:k]

if __name__ == "__main__":
    top_k_profiles = topk_googlescholar(8, "Seattle")
    write_profile_to_csv(top_k_profiles)
    for profile in top_k_profiles:
        print(f"Name: {profile['name']}\n relevance: {profile['relevance_score']}\n citations: {profile['citations']}\n H-index: {profile['h_index']}\n Degree/Institute of Work: {profile['degree_type']}\n Profile Link: {profile['scholar_url']}\n Linkedin: {profile['Linkedin']}\n")
