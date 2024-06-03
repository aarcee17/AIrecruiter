import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

def get_professor_url(prof_name, university):
    """ Get the Google Scholar URL for a professor """
    query = f"{prof_name} {university} Google Scholar"
    for url in search(query, num_results= 5):
        if 'scholar.google.com/citations?' in url:
            return url
    return None

def get_authors_from_citation(citation_url):
    """ Extract authors using BeautifulSoup from the given publication page """
    response = requests.get(citation_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch publication page: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    author_element = soup.find('div', class_='gsc_oci_value')
    if author_element:
        authors = author_element.text
        return authors.split(", ")
    return []

def get_citation_links(prof_url):
    """ Extract citation links from the professor's Google Scholar profile page """
    base_url = "https://scholar.google.com"
    response = requests.get(prof_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch profile page: {response.status_code}")

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

# def main():
#     prof_name = input("Enter the professor's name: ")
#     university = input("Enter the university: ")
#     prof_url = get_professor_url(prof_name, university)

#     if prof_url:
#         print(f"Found Google Scholar URL: {prof_url}")
#         citation_links = get_citation_links(prof_url)
#         all_authors = []
        
#         for link in citation_links:
#             authors = get_authors_from_citation(link)
#             all_authors.extend(authors)
#             time.sleep(1)  # Respect rate limits

#         unique_authors = set(all_authors)
#         formatted_authors = [(author, prof_name, university) for author in unique_authors]
#         print("Extracted authors:")
#         for author in formatted_authors:
#             print(author)
#     else:
#         print("Google Scholar URL not found.")

# if __name__ == "__main__":
#     main()
def main():
    prof_name = input("Enter the professor's name: ")
    university = input("Enter the university: ")
    prof_url = get_professor_url(prof_name, university)
    print(prof_url)
    print("\nfound")
    citation_links = get_citation_links(prof_url)
    print(citation_links)
    
    
    
    
    
    
    
if __name__ == "__main__":
    
    main()    