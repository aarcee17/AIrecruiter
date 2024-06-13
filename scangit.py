import requests
import numpy as np
from github import score_github_user
from linkedin import fetch_linkedin_url
import time
def fetch_topkgithub(k, location=None):
    database = []
    #queries = ["ML+Architect", "AI+Architect", "NLP+engineer"]
    queries = ["ML+engineer", "AI+engineer", "ML+Research", "AI+Research"]
    #queries = ["ML", "AI", "PhD+ML", "PhD+AI", "ML+engineer", "AI+engineer", "ML+researcher", "AI+researcher"]
    for query in queries:
        if location:
            queryy =query + f"+{location}"
        
        url = f"https://github.com/search?q={queryy}&type=users"
        urll = f"https://github.com/search?q=location%3A{location}+repos%3A%3E3+{query}&type=users&ref=advsearch"
        print(url)
        print(urll)
        response = requests.get(url)
        time.sleep(1)
        if response.status_code != 200:
            print("error url")
            raise Exception(f"Failed to fetch GitHub search page: {response.status_code}")

        data = response.json()
        user_logins = [user['login'] if user['login'][0] != '<' else user['login'][3:-4] for user in data['payload']['results']]
        database += user_logins
        time.sleep(2)
        response = requests.get(urll)
        time.sleep(2)
        if response.status_code != 200:
            print("error urll")
            raise Exception(f"Failed to fetch GitHub search page: {response.status_code}")

        data = response.json()
        time.sleep(2)
        user_logins = [user['login'] if user['login'][0] != '<' else user['login'][3:-4] for user in data['payload']['results']]
        database += user_logins
        time.sleep(2)

    database = set(database)
    
    
    github_profiles = []
    scores = []
    
    for github_id in database:
        total_score, details, detailed_scores = score_github_user(github_id)
        github_profiles.append({
            'github_id': github_id,
            'name': details.name,
            'bio': details.bio,
            'location': details.location,
            'linkedin': details.linkedin_url,
            'total_score': total_score+1,
        })
        scores.append(total_score)
    for profile in github_profiles:
        if profile['total_score'] ==0:
            github_profiles.remove(profile)
            
    mean_score = np.mean(scores)
    std_dev_score = np.std(scores)
    
    for profile in github_profiles:
        normalized_score = 75 + 25 * ((profile['total_score'] - mean_score) / std_dev_score)
        profile['normalized_score'] = normalized_score

    sorted_profiles = sorted(github_profiles, key=lambda x: x['normalized_score'], reverse=True)
    return sorted_profiles

import csv
def write_github_to_csv(sorted_profiles):
    
    with open('github_profiles.csv', 'w') as csvfile:           
        fieldnames = ['github_id', 'name', 'bio', 'location', 'linkedin', 'total_score', 'normalized_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for profile in sorted_profiles:
            writer.writerow(profile)

if __name__ == "__main__":
    top_k_profiles = fetch_topkgithub(8, "USA")
    write_github_to_csv(top_k_profiles)
    for profile in top_k_profiles:
        print(f"GitHub ID: {profile['github_id']}\n Name: {profile['name']}\n Normalized Score: {profile['normalized_score']}\n Total Score: {profile['total_score']}\n Bio: {profile['bio']}\n Location: {profile['location']}\n LinkedIn: {profile['linkedin']}\n")
