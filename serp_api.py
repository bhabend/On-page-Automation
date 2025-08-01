import requests

SERP_API_KEY = 'YOUR_SERPHOUSE_API_KEY'  # <-- Replace with your actual API key

def get_serp_data(keyword, location='us', language='en'):
    url = "https://api.serphouse.com/serp/live"
    payload = {
        "api_key": SERP_API_KEY,
        "q": keyword,
        "gl": location,
        "hl": language,
        "num": 10
    }
    response = requests.post(url, json=payload)
    results = response.json()
    
    if 'organic' in results.get('data', {}):
        return [{"position": item['position'], "title": item['title'], "url": item['url']} for item in results['data']['organic']]
    else:
        return []
