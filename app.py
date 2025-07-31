import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

st.title("On-Page SEO Automation Tool")

urls_input = st.text_area("Enter URLs (one per line):")
urls = [url.strip() for url in urls_input.split("\n") if url.strip()]

def fetch_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        content = page.content()
        browser.close()
        return content

if not urls:
    st.warning("Please enter at least one URL.")
else:
    results = []

    for url in urls:
        try:
            html_content = fetch_page_content(url)
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract SEO Elements
            title_tag = soup.title.get_text(strip=True) if soup.title and soup.title.get_text(strip=True) else 'MISSING'
            title_len = len(title_tag.encode('utf-8')) if title_tag != 'MISSING' else 0

            meta_tag = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_tag.get('content', '').strip() if meta_tag else 'MISSING'
            meta_len = len(meta_description.encode('utf-8')) if meta_description != 'MISSING' else 0

            canonical_tag = soup.find('link', rel='canonical')
            canonical_url = canonical_tag.get('href', '').strip() if canonical_tag else 'MISSING'

            h1_tag = soup.find('h1')
            h1_text = h1_tag.get_text(strip=True) if h1_tag else 'MISSING'

            images = soup.find_all('img')
            missing_alts = [img.get('src') for img in images if not img.get('alt')]

            title_status = 'OK' if 50 <= title_len <= 60 else 'Too Short' if title_len < 50 else 'Too Long'
            meta_status = 'OK' if 150 <= meta_len <= 160 else 'Too Short' if meta_len < 150 else 'Too Long'

            results.append({
                'URL': url,
                'Title': title_tag,
                'Title Length': title_len,
                'Title Status': title_status,
                'Meta Description': meta_description,
                'Meta Length': meta_len,
                'Meta Status': meta_status,
                'H1 Tag': h1_text,
                'Canonical Tag': canonical_url,
                'Missing ALT Images Count': len(missing_alts),
            })

        except Exception as e:
            results.append({
                'URL': url,
                'Title': 'ERROR',
                'Title Length': 'ERROR',
                'Title Status': 'ERROR',
                'Meta Description': 'ERROR',
                'Meta Length': 'ERROR',
                'Meta Status': 'ERROR',
                'H1 Tag': 'ERROR',
                'Canonical Tag': 'ERROR',
                'Missing ALT Images Count': 'ERROR'
            })

    df = pd.DataFrame(results)
    st.success("Audit Complete! Download your report below.")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name='onpage_seo_audit.csv', mime='text/csv')
