import requests
from bs4 import BeautifulSoup
from github import score_github_user
from linkedin import fetch_linkedin_url

def fetch_topkgithub(k, location=None):
    database = []
    #queries = ["ML Architect","AI Architect","GenAI","Generative AI"]
    queries = ["ML","AI","PhD ML","PhD AI","ML engineer","AI engineer","ML researcher","AI researcher"]
    for query in queries:
        
        if location:
            query += f" {location}"
        
        url = f"https://github.com/search?q={query}&type=users"
        #print("Fetching GitHub search page...")
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch GitHub search page: {response.status_code}")

        data = response.json()
        #print(data)
        user_logins = []
        for user in data['payload']['results']:
            if(user['login'][0]!= '<'):
                user_logins.append(user['login'])
            else:
                user_logins.append(user['login'][3:-4])    
            #user_logins = ([user['login'] for user in data['payload']['users'][:k]])
        # user_logins = ([user['hl_login'] for user in data['payload']['results'][:k]]) 
        database+=user_logins
        #print(user_logins)
    #print(database)
    database = set(database)    
    github_profiles = []
    for github_id in database:
        total_score,details, detailed_scores = score_github_user(github_id)
        github_profiles.append({
            'github_id': github_id,
            'name': details.name,
            'bio': details.bio,
            'location': details.location,
            'linkedin': details.linkedin_url,
            'total_score': total_score,
            
            #'detailed_scores': detailed_scores,
            #'linkedin': fetch_linkedin_url(github_id, )
        })

    sorted_profiles = sorted(github_profiles, key=lambda x: x['total_score'], reverse=True)
    #sorted_profiles = sorted_profiles[:k]
    return sorted_profiles
import csv
def write_github_to_csv(sorted_profiles):
    with open('github_profiles.csv', 'w') as csvfile:
        fieldnames = ['github_id', 'name','bio','location','linkedin', 'total_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for profile in sorted_profiles:
            writer.writerow(profile)

if __name__ == "__main__":
    top_k_profiles = fetch_topkgithub(8, "seattle")
    #write_github_to_csv(top_k_profiles)
    for profile in top_k_profiles:
        print(f"GitHub ID: {profile['github_id']},Name: {profile['name']},Bio: {profile['bio']},Location: {profile['location']}, LinkedIn: {profile['linkedin']}, Total Score: {profile['total_score']}")
        #print(f"GitHub ID: {profile['github_id']},Detials: {profile['details']} Total Score: {profile['total_score']}")
        # for repo in profile['detailed_scores']:
        #     print(f"  Repo: {repo['name']}, Score: {repo['score']}, Stars: {repo['stars']}, Relevance Score: {repo['relevance_score']}")

    