import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc['content'] if meta_desc else ''

        h1 = soup.find('h1')
        h1_text = h1.get_text().strip() if h1 else ''

        return f"Title: {title}\nDescription: {meta_desc}\nH1: {h1_text}"
    except:
        return "Content fetch failed."
