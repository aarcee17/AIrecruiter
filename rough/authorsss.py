import requests
from bs4 import BeautifulSoup

def get_professor_page(url):
    """ Fetch the HTML content of the professor's main page """
    try:
        response = requests.get(url)
        response.raise_for_status()  # will raise an exception for 4XX/5XX errors
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_publication_links(soup):
    """ Extract links to publications from the main page """
    base_url = "https://scholar.google.com"
    links = []
    if soup:
        for link in soup.find_all('a', class_='gsc_a_t'):
            href = link.get('href')
            full_url = base_url + href
            links.append(full_url)
            if len(links) == 15:
                break
    return links

def fetch_authors_from_publication(url):
    """ Fetch authors from a specific publication page """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        author_text = soup.find('div', class_='gsc_oci_value').text
        authors = author_text.split(", ")
        return authors
    except requests.RequestException as e:
        print(f"Failed to fetch publication: {e}")
        return []

def main(prof_url):
    soup = get_professor_page(prof_url)
    publication_links = extract_publication_links(soup)
    all_authors = []

    for link in publication_links:
        authors = fetch_authors_from_publication(link)
        all_authors.extend(authors)
    
    unique_authors = set(all_authors)
    formatted_authors = [(author, "Prof Name", "University Name") for author in unique_authors]
    return formatted_authors

if __name__ == "__main__":
    professor_url = 'https://scholar.google.com/citations?user=5y4YmFcAAAAJ&hl=en&oi=ao'  # Replace with actual URL
    authors_list = main(professor_url)
    print("Extracted authors:")
    for author in authors_list:
        print(author)
