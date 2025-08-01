from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin

def fetch_page_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string.strip() if soup.title else "No title found"
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag["content"].strip() if meta_desc_tag and "content" in meta_desc_tag.attrs else "No meta description"

    canonical_tag = soup.find("link", rel="canonical")
    canonical_url = canonical_tag["href"] if canonical_tag and "href" in canonical_tag.attrs else "No canonical tag"

    word_count = len(soup.get_text().split())

    images = soup.find_all("img")
    image_count = len(images)
    images_missing_alt = [img for img in images if not img.get("alt")]

    links = soup.find_all("a", href=True)
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc

    internal_links = [a["href"] for a in links if urlparse(urljoin(url, a["href"])).netloc == base_domain]
    external_links = [a["href"] for a in links if urlparse(urljoin(url, a["href"])).netloc != base_domain]

    headings = {}
    for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        headings[tag] = [h.get_text(strip=True) for h in soup.find_all(tag)]

    return {
        "title": title,
        "meta_description": meta_desc,
        "canonical_url": canonical_url,
        "word_count": word_count,
        "image_count": image_count,
        "images_missing_alt": images_missing_alt,
        "internal_links": internal_links,
        "external_links": external_links,
        "headings": headings,
    }

def audit_seo_rules(data):
    score = 100
    issues = []

    if len(data.get('title', '')) > 60:
        issues.append("Title tag is too long.")
        score -= 5

    if data.get('meta_description') == "No meta description":
        issues.append("Missing meta description.")
        score -= 5

    if data.get('canonical_url') == "No canonical tag":
        issues.append("Missing canonical URL.")
        score -= 5

    missing_alts = data.get('images_missing_alt', [])
    if len(missing_alts) > 0:
        issues.append("Some images are missing alt attributes.")
        score -= 5

    if data.get('word_count', 0) < 300:
        issues.append("Low word count.")
        score -= 5

    if len(data.get('headings', {}).get("h1", [])) != 1:
        issues.append("There should be exactly one H1 tag.")
        score -= 5

    if len(data.get('internal_links', [])) < 3:
        issues.append("Too few internal links.")
        score -= 5

    return max(score, 0), issues
