import requests

class PerplexityAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/v1/scrape"

    def scrape_webpage(self, url):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.base_url, json={"url": url}, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
