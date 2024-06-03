import requests
from bs4 import BeautifulSoup
from googlesearch import search
#from googlescholar import fetch_scholar_data

def search_github_username(name, university):
    query = f"{name} {university} GitHub"
    for url in search(query, num_results=5):
        if 'github.com' in url:
            return url.split('/')[-1]
    return "nope not found"

def main():
    print(search_github_username("Rim Assouel", "University De Montreal"))
    
if __name__ == "__main__":
    main()    
    