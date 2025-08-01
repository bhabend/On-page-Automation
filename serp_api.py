import os
import requests

SERP_API_KEY = os.getenv('SERPAPI_KEY')

def get_serp_data(keyword, location='us', language='en'):
    if not SERP_API_KEY:
        raise ValueError("SERPAPI_KEY is not set in environment variables.")

    params = {
        "engine": "google",
        "q": keyword,
        "location": location,
        "hl": language,
        "num": "10",
        "api_key": SERP_API_KEY
    }

    url = "https://serpapi.com/search.json"
    response = requests.get(url, params=params)
    results = response.json()

    if 'organic_results' in results:
        return [{"position": item['position'], "title": item['title'], "url": item['link']} for item in results['organic_results']]
    else:
        print("SerpAPI Response:", results)  # Debugging line to see API response in Render Logs
        return []
