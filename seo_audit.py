from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def audit_seo(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title else "Missing"
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag["content"].strip() if meta_desc_tag else "Missing"
    canonical = soup.find("link", rel="canonical")
    canonical = canonical["href"] if canonical else "Missing"
    h_tags = {f"H{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 7)}
    images = soup.find_all("img")
    missing_alts = [img for img in images if not img.get("alt")]
    links = soup.find_all("a", href=True)

    internal_links, external_links = 0, 0
    domain = urlparse(base_url).netloc
    for link in links:
        href = urlparse(link['href'])
        if href.netloc and href.netloc != domain:
            external_links += 1
        else:
            internal_links += 1

    word_count = len(soup.get_text().split())

    return {
        "Title": title,
        "Meta Description": meta_desc,
        "Canonical": canonical,
        "Word Count": word_count,
        "Image Count": len(images),
        "Missing Alts": len(missing_alts),
        "Internal Links": internal_links,
        "External Links": external_links,
        "H Tags": h_tags,
    }
