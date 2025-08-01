import os
import requests

SERP_API_KEY = os.getenv('SERPAPI_KEY')

def get_serp_data(keyword, language='en'):
    if not SERP_API_KEY:
        raise ValueError("SERPAPI_KEY is not set in environment variables.")

    params = {
        "engine": "google",
        "q": keyword,
        "hl": language,
        "num": "10",
        "api_key": SERP_API_KEY
    }

    url = "https://serpapi.com/search.json"
    response = requests.get(url, params=params)
    results = response.json()

    if 'organic_results' in results:
        return [{"position": item.get('position'), "title": item.get('title'), "url": item.get('link')} for item in results['organic_results']]
    else:
        print("SerpAPI Response Error:", results)
        return []
