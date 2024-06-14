import requests
from googlesearch import search
from scangit import *
from scangs import *
from filter import *
from prof import *
import sys
from combiner import *
from llm import *
def classify_query(query):
    
    locations = [loc.lower() for loc in qlocations]
    classification = {"github": False, "scholar": False, "student": False, "location": None}
    words = query.lower().split()
    for word in words:
        if word in locations:
            classification["location"] = word
        if any(keyword in query.lower() for keyword in github_keywords):
            classification["github"] = True
        if any(keyword in query.lower() for keyword in scholar_keywords):
            classification["scholar"] = True
        if any(keyword in query.lower() for keyword in student_keywords):
            classification["student"] = True

    return classification

def process_query(query):
    classification = classify_query(query)

    categories = []
    if classification["github"]:
        #print("github")
        categories.append("github")
    if classification["scholar"]:
        #print("scholar")
        categories.append("scholar")
    if classification["student"]:
        #print("student")
        categories.append("student")
    location = classification["location"]
    print(location)
    return categories, location
#AI architect Pan US, LLM, vectors, 
def extract_parameters(query):
    k = 7

    words = query.split()
    for i, word in enumerate(words):
        if word.isdigit():
            k = int(word)
        elif word.lower() == "top" and i < len(words) - 1 and words[i+1].isdigit():
            k = int(words[i+1])
    #print("detected k = {k}")        
    return k         

def find_colleges(location):
    colleges = []
    for university, details in professors.items():
        for detail in details:
            if detail.get('location',None) == location:
                colleges.append(university)
    return colleges
    
    
# Example usage
queries = ' '.join(sys.argv[1:])
list_queries = queries.split(",")
for query in list_queries:
    categories, location = process_query(query)
    k = extract_parameters(query)

    for category in categories:
        if category == "github":
            #print("Finding top {k} GitHub profiles in {location}...".format(k=k, location=location))
            top_k_profiles = fetch_topkgithub(k, location)
            write_github_to_csv(top_k_profiles)
            
            for profile in top_k_profiles:
                print(f"GitHub ID: {profile['github_id']}\n Link: https://github.com/{profile['github_id']}\n  Total Score: {profile['total_score']}\n")
        elif category == "scholar":
            #print("Finding top {k} scholars in {location}...".format(k=k, location=location))
            top_k_profiles = topk_googlescholar(k, location)
            #write_profile_to_csv(top_k_profiles)
            for profile in top_k_profiles:
                print(f"Name: {profile['name']}\n relevance: {profile['relevance_score']}\n citations: {profile['citations']}\n H-index: {profile['h_index']}\n Degree/Institute of Work: {profile['degree_type']}\n Profile Link: {profile['scholar_url']}\n Linkedin Link: {profile['Linkedin']}\n")
        elif category == "student":
            #print("Finding top {k} students in {location}...".format(k=k, location=location))
            colleges = find_colleges(location)
            for college in colleges:
                remain(college, k)
                time.sleep(2)

# github_file = 'datalog/github_profiles.csv' 
# authors_file = 'datalog/filtered_authors.csv' 
# scholars_file = 'datalog/scholar.csv' 
# output_file = 'datalog/merged_output.csv' 
    
#merge_csv_files(github_file, authors_file, scholars_file, output_file)
#print(f"Merged CSV files written to {output_file}")