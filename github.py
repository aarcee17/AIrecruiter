import requests
from bs4 import BeautifulSoup
from rank_bm25 import BM25Okapi
import numpy as np
import re
def extract_numeric(text):
    match = re.search(r'\d+', text.replace(',', ''))
    return int(match.group()) if match else 0
# Example corpus for BM25
ai_ml_corpus = [
    "machine learning", "artificial intelligence", "deep learning", "neural networks",
    "supervised learning", "unsupervised learning", "reinforcement learning", "data science",
    "computer vision", "natural language processing", "AI architecture", "MLOps", "robotics",
    "autonomous systems", "big data", "data mining", "predictive analytics", "algorithm development",
    "pattern recognition", "speech recognition", "image processing", "tensor operations", "model training",
    "hyperparameter tuning", "model evaluation", "feature engineering", "data preprocessing",
    "model deployment", "cloud computing", "distributed computing", "parallel computing", "GPU acceleration",
    "neural architecture search", "transfer learning", "meta learning", "self-supervised learning",
    "semi-supervised learning", "explainable AI", "AI ethics", "federated learning", "adversarial learning",
    "generative models", "transformer models", "BERT", "GPT", "computer graphics", "genetic algorithms",
    "support vector machines", "ensemble methods", "time series analysis", "dimensionality reduction",
    "clustering algorithms", "transformers", "attention models", "recurrent neural networks", "LSTM"
]

bm25 = BM25Okapi([doc.split() for doc in ai_ml_corpus])

class RepoDetails:
    def __init__(self, name, stars, description, language, forks, last_updated):
        self.name = name
        self.stars = stars
        self.description = description
        self.language = language
        self.forks = forks
        self.last_updated = last_updated

class UserGitHubDetails:
    def __init__(self, username):
        self.username = username
        self.name = None
        self.bio = None
        self.location = None
        self.organization = None
        self.linkedin_url = "URL not found"
        #self.contributions = 0
        self.repositories = []

    def fetch_profile_details(self):
        url = f"https://github.com/{self.username}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user profile: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        self.name = soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden').text.strip() if soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden') else None
        self.bio = soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4').text.strip() if soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4') else None
        self.location = soup.find('span', class_='p-label').text.strip() if soup.find('span', class_='p-label') else None
        self.organization = soup.find('span', class_='p-org').text.strip() if soup.find('span', class_='p-org') else None
        

        linkedin_element = soup.find('a', class_='Link--primary', rel='nofollow me')
        if linkedin_element and 'linkedin.com' in linkedin_element['href']:
            self.linkedin_url = linkedin_element['href']
        
        
        #print("hihj")
        # contributions_element = soup.find('h2', class_='f4 text-normal mb-2')
        # if contributions_element:
        #     print("yes")
        #     contributions_text = contributions_element.get_text(strip=True).split()[0]
        #     self.contributions = int(contributions_text.replace(',', ''))

    def fetch_repositories(self):
        page = 1
        while True:
            url = f"https://github.com/{self.username}?page={page}&tab=repositories"
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch repositories: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            repos = soup.find_all('li', class_='col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public fork')
            repos += soup.find_all('li', class_='col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source')
            if len(repos) > 20:
                repos = repos[:20]
            if not repos:
                break

            for repo in repos:
                name = repo.find('a', itemprop='name codeRepository').text.strip()
                stars_element = repo.find('a', class_='Link--muted mr-3')
                stars_text = stars_element.text.strip() if stars_element else "0"
                stars = extract_numeric(stars_text)
                description_element = repo.find('p', itemprop='description')
                description = description_element.text.strip() if description_element else None
                language_element = repo.find('span', itemprop='programmingLanguage')
                language = language_element.text.strip() if language_element else None
                forks_element = repo.find('a', href=lambda href: href and 'network/members' in href)
                forks = int(forks_element.text.strip().replace(',', '')) if forks_element else 0
                last_updated_element = repo.find('relative-time')
                last_updated = last_updated_element['datetime'] if last_updated_element else None
                self.repositories.append(RepoDetails(name, stars, description, language, forks, last_updated))
            
            page += 1

    def fetch_all_details(self):
        self.fetch_profile_details()
        self.fetch_repositories()

def score_repositories(repo_data):
    scores = []
    for repo in repo_data:
        stars_score = repo['stars']
        tokenized_description = repo['description'].split() if repo['description'] else []
        project_relevance_score = sum(bm25.get_scores(tokenized_description)) + 10*sum(bm25.get_scores(repo['name'].split()))
        total_score = np.log(stars_score + 2) * (project_relevance_score + 1)
        scores.append({
            'name': repo['name'],
            'score': total_score,
            'stars': repo['stars'],
            'description': repo['description'],
            'language': repo['language'],
            'forks': repo['forks'],
            'last_updated': repo['last_updated'],
            'relevance_score': project_relevance_score
        })
    return scores

def aggregate_scores(scores):
    total_score = sum(repo['score'] for repo in scores)
    return total_score

def bio_score(bio):
    tokenized_description = bio.split() if bio else []
    brs = sum(bm25.get_scores(tokenized_description))
    return brs

def score_github_user(username):
    user_details = UserGitHubDetails(username)
    user_details.fetch_all_details()
    
    repo_data = []
    for repo in user_details.repositories:
        repo_data.append({
            'name': repo.name,
            'stars': repo.stars,
            'description': repo.description,
            'language': repo.language,
            'forks': repo.forks,
            'last_updated': repo.last_updated
        })
    
    scores = score_repositories(repo_data)
    total_score = aggregate_scores(scores) + 10 * bio_score(user_details.bio)**2
    return total_score, user_details, scores

def main():
    username = input("Enter the GitHub username: ")
    try:
        total_score, user_profile, detailed_scores = score_github_user(username)
        print(f"Total GitHub Score for {username}: {total_score}")
        print("User Profile:")
        print(f"Username: {user_profile.username}")
        print(f"Name: {user_profile.name}")
        print(f"Bio: {user_profile.bio}")
        print(f"Location: {user_profile.location}")
        print(f"Organization: {user_profile.organization}")
        print(f"LinkedIn URL: {user_profile.linkedin_url}")
        #print(f"Contributions (Last Year): {user_profile.contributions}")
        print("\nDetailed Scores:")
        for score in detailed_scores:
            print(f"Repository: {score['name']}")
            print(f"  Score: {score['score']}")
            print(f"  Stars: {score['stars']}")
            print(f"  Description: {score['description']}")
            print(f"  Language: {score['language']}")
            print(f"  Forks: {score['forks']}")
            print(f"  Last Updated: {score['last_updated']}")
            print(f"  Relevance Score: {score['relevance_score']}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
