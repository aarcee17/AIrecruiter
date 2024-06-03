import requests
from bs4 import BeautifulSoup

class RepoDetails:
    def __init__(self, name, stars, description):
        self.name = name
        self.stars = stars
        self.description = description
#col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source
   # def __repr__(self):
       # return f"RepoDetails(name={self.name}, stars={self.stars}, description={self.description})"

class UserGitHubDetails:
    def __init__(self, username):
        self.username = username
        self.name = None
        self.bio = None
        self.location = None
        self.organization = None
        self.repositories = []

   # def __repr__(self):
       # return (f"UserGitHubDetails(username={self.username}, name={self.name}, bio={self.bio}, "
              #  f"location={self.location}, organization={self.organization}, repositories={self.repositories})")

    def fetch_profile_details(self):
        url = f"https://github.com/{self.username}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user profile: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
#col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source
        self.name = soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden').text.strip() if soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden') else None
        self.bio = soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4').text.strip() if soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4') else None
        self.location = soup.find('span', class_='p-label').text.strip() if soup.find('span', class_='p-label') else None
        self.organization = soup.find('span', class_='p-org').text.strip() if soup.find('span', class_='p-org') else None

    def fetch_repositories(self):
        page = 1
        while True:
            url = f"https://github.com/{self.username}?page={page}&tab=repositories"
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch repositories: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            repos = soup.find_all('li', class_='col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public fork')
            repos+= soup.find_all('li', class_='col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source')

            if not repos:
                break

            for repo in repos:
                name = repo.find('a', itemprop='name codeRepository').text.strip()
                stars_element = repo.find('a', class_='Link--muted mr-3')
                stars = int(stars_element.text.strip().replace(',', '')) if stars_element else 0
                description_element = repo.find('p', itemprop='description')
                description = description_element.text.strip() if description_element else None
                self.repositories.append(RepoDetails(name, stars, description))
            
            page += 1

    def fetch_all_details(self):
        self.fetch_profile_details()
        self.fetch_repositories()
