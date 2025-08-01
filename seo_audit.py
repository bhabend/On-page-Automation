import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

# 🔐 Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# 🌐 Fetches HTML and basic page info
def fetch_page_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Title
    title = soup.title.string.strip() if soup.title else "No title"

    # Meta Description
    description_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = description_tag["content"].strip() if description_tag and description_tag.get("content") else "No meta description"

    # Canonical
    canonical_tag = soup.find("link", rel="canonical")
    canonical_url = canonical_tag["href"].strip() if canonical_tag and canonical_tag.get("href") else "No canonical tag"

    # Headings
    headings = {f'h{i}': [tag.get_text(strip=True) for tag in soup.find_all(f'h{i}')] for i in range(1, 7)}

    # Images
    images = soup.find_all("img")
    images_missing_alt = [img for img in images if not img.get("alt")]
    image_count = len(images)

    # Word Count
    page_text = soup.get_text()
    words = page_text.split()
    word_count = len(words)

    # Links
    internal_links = []
    external_links = []
    base_domain = urlparse(url).netloc

    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["h]()
