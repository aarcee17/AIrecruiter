import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import random
from fake_useragent import UserAgent

ua = UserAgent()

def get_professor_url(prof_name, university):

    query = f"{prof_name} {university} Google Scholar"
    for url in search(query, num_results= 5):
        if 'scholar.google.com/citations?' in url:
            return url
    return None

def get_response_with_retries(url, retries=5, backoff_factor=1):

    headers = {'User-Agent': ua.random}
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            time.sleep(backoff_factor * (2 ** attempt) + random.uniform(0, 1))
        else:
            response.raise_for_status()
    raise Exception(f"fail after {retries} retries")

def get_authors_from_citation(citation_url):

    response = get_response_with_retries(citation_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    author_element = soup.find('div', class_='gsc_oci_value')
    if author_element:
        authors = author_element.text
        return authors.split(", ")
    return []

def get_citation_links(prof_url):
   
    base_url = "https://scholar.google.com"
    response = get_response_with_retries(prof_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    citation_links = []

    for row in soup.select('tr.gsc_a_tr'):
        link = row.find('a', class_='gsc_a_at')
        if link:
            href = link['href']
            full_url = base_url + href
            citation_links.append(full_url)
            if len(citation_links) == 15:  # Limit to the first 15 links
                break

    return citation_links

def main():
    prof_name = input("professor's name: ")
    university = input("university: ")
    prof_url = get_professor_url(prof_name, university)

    if prof_url:
        print(f"GS url: {prof_url}")
        citation_links = get_citation_links(prof_url)
        all_authors = []

        for link in citation_links:
            authors = get_authors_from_citation(link)
            all_authors.extend(authors)
            time.sleep(1)  

        unique_authors = set(all_authors)
        formatted_authors = [(author, prof_name, university) for author in unique_authors]
        print("authors:")
        for author in formatted_authors:
            print(author)
    else:
        print("no url")

# if __name__ == "__main__":
#     main()
