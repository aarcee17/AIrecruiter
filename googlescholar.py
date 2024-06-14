import requests
from bs4 import BeautifulSoup
import time
import math
from rank_bm25 import BM25Okapi
from googlesearch import search
from llm import gs_ai_ml_corpus
def tokenize(text):
    return text.lower().split()

def fetch_scholar_data(scholar_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    max_retries = 5
    for attempt in range(max_retries):
        response = requests.get(scholar_url, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            time.sleep(10)
        else:
            raise Exception(f"Failed to fetch the webpage. Status code: {response.status_code}")
    else:
        raise Exception("Max retries exceeded. Could not fetch the webpage.")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    metrics = {}

    item = soup.select_one('#gsc_prf_in')
    if item:
        metrics['name'] = item.text.strip()
    else:
        print("Name element not found")

    for item in soup.select('#gsc_rsb_st td'):
        try:
            text = item.text.strip()
            if 'Citations' in text:
                metrics['citations'] = int(item.find_next_sibling('td').text.strip())
            if 'h-index' in text:
                metrics['h_index'] = int(item.find_next_sibling('td').text.strip())
            if 'i10-index' in text:
                metrics['i10_index'] = int(item.find_next_sibling('td').text.strip())
        except:
            continue

    description = ''
    for item in soup.select('#gsc_prf_bio'):
        description = item.text.strip()

    if not description:
        for item in soup.select('#gsc_prf_int'):
            description = item.text.strip()
            
    tokenized_prompts = [tokenize(prompt) for prompt in gs_ai_ml_corpus]
    bm25 = BM25Okapi(tokenized_prompts)

    if description:
        tokenized_description = tokenize(description)
        relevance_scores = bm25.get_scores(tokenized_description)
        relevance_score = sum(relevance_scores) / len(relevance_scores)
    else:
        relevance_score = 0

    metrics['relevance_score'] = relevance_score*metrics.get('h_index', 1)*math.sqrt(metrics.get('citations', 1000))/545.70

    return metrics

def get_google_scholar_url(prof_name, college):    
    query = f"Professor {prof_name} {college} Google Scholar"
    for url in search(query, num_results=10):
        if 'scholar.google.com/citations' in url:
            return url
    return None

if __name__ == "__main__":
    prof_name = "Yoshua Bengio"
    college = "Université de Montréal"
    scholar_url = get_google_scholar_url(prof_name, college)
    if scholar_url:
        scholar_data = fetch_scholar_data(scholar_url)
        print(scholar_data)
    else:
        print("Google Scholar profile not found.")
