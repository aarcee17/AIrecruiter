import requests
from bs4 import BeautifulSoup
from github import score_github_user
from linkedin import fetch_linkedin_url
def fetch_topkgithub(k, location=None):
    database = []
    queries = ["ML","AI","PhD ML","PhD AI"]
    for query in queries:
        
        if location:
            query += f" {location}"
        
        url = f"https://github.com/search?q={query}&type=users"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch GitHub search page: {response.status_code}")

        data = response.json()
        #print(data)
        user_logins = []
        for user in data['payload']['results'][:k]:
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
            'total_score': total_score,
            'detailed_scores': detailed_scores,
            #'linkedin': fetch_linkedin_url(github_id, )
        })

    sorted_profiles = sorted(github_profiles, key=lambda x: x['total_score'], reverse=True)
    sorted_profiles = sorted_profiles[:k]
    return sorted_profiles


if __name__ == "__main__":
    top_k_profiles = fetch_topkgithub(12, "Boston")
    for profile in top_k_profiles:
        print(f"GitHub ID: {profile['github_id']}, Total Score: {profile['total_score']}")
        for repo in profile['detailed_scores']:
            print(f"  Repo: {repo['name']}, Score: {repo['score']}, Stars: {repo['stars']}, Relevance Score: {repo['relevance_score']}")
