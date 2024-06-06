import requests
from bs4 import BeautifulSoup
from googlesearch import search

def fetch_linkedin_url(name, workplace, retries=5):
    query = f"{name} {workplace} LinkedIn"
    search_url = None
    for url in search(query, num_results=10, lang="en"):
        if "linkedin.com/in/" in url:
            search_url = url
            break

    if search_url:
        return search_url
    else:
        return "not found"

if __name__ == "__main__":
    name = input("Enter the person's name: ")
    workplace = input("Enter the workplace: ")

    linkedin_url = fetch_linkedin_url(name, workplace)
    print(f"LinkedIn URL: {linkedin_url}")
