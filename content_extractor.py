import requests
from bs4 import BeautifulSoup

def extract_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "Failed to fetch content."

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract main textual content
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])

        return content.strip() if content else "No meaningful content found."
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return "Error fetching content."
