import requests
from googlesearch import search
from scangit import fetch_topkgithub
from scangs import topk_googlescholar
from scanauth import *
from prof import *
import sys
from llm import names_list,specific_locations
categories = input("Enter category: ").split(", ")
k = int(input("Enter number of profiles to fetch: "))

specific_locations+=names_list
def fetch_unique_scholar_profiles(k, locations):
    all_profiles = []
    seen_profiles = {}

    for location in locations:
        top_k_profiles = topk_googlescholar(k, location)
        for profile in top_k_profiles:
            identifier = profile['scholar_url']
            if identifier not in seen_profiles:
                seen_profiles[identifier] = profile

    unique_profiles = list(seen_profiles.values())
    return unique_profiles

def fetch_unique_github_profiles(k, locations):
    all_profiles = []
    seen_profiles = {}

    for location in locations:
        top_k_profiles = fetch_topkgithub(k, location)
        for profile in top_k_profiles:
            identifier = profile['github_id']
            if identifier not in seen_profiles:
                seen_profiles[identifier] = profile

    unique_profiles = list(seen_profiles.values())
    return unique_profiles
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
            
            
for category in categories:
    if category == "github":
        unique_profiles = fetch_unique_github_profiles(k, specific_locations)
        for profile in unique_profiles:
            print(f"GitHub ID: {profile['github_id']}\nLink: https://github.com/{profile['github_id']}\nTotal Score: {profile['total_score']}\n")
    elif category == "scholar":
        unique_profiles = fetch_unique_scholar_profiles(k, specific_locations)
        for profile in unique_profiles:
            print(f"Name: {profile['name']}\nRelevance: {profile['relevance_score']}\nCitations: {profile['citations']}\nH-index: {profile['h_index']}\nDegree/Institute of Work: {profile['degree_type']}\nProfile Link: {profile['scholar_url']}\nLinkedin Link: {profile['Linkedin']}\n")
