import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_page_data(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else ""
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag["content"].strip() if meta_desc_tag else ""

    headings = {
        f"{tag.name}": [h.get_text(strip=True) for h in soup.find_all(tag.name)]
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    }

    images = soup.find_all("img")
    image_count = len(images)
    images_missing_alt = [img.get('src') for img in images if not img.get('alt')]

    links = soup.find_all("a", href=True)
    internal_links = [a['href'] for a in links if urlparse(a['href']).netloc == '']
    external_links = [a['href'] for a in links if urlparse(a['href']).netloc != '']

    canonical_tag = soup.find("link", rel="canonical")
    canonical_url = canonical_tag["href"] if canonical_tag else ""

    word_count = len(soup.get_text().split())

    return {
        "title": title,
        "meta_description": meta_desc,
        "headings": headings,
        "word_count": word_count,
        "image_count": image_count,
        "images_missing_alt": images_missing_alt,
        "internal_links": internal_links,
        "external_links": external_links,
        "canonical_url": canonical_url,
        "status": "success"
    }
