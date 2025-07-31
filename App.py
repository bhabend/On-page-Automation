import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("On-Page SEO Automation Tool")

# URL Input Box
urls_input = st.text_area("Enter URLs (one per line)", height=200)
urls = urls_input.strip().split('\n') if urls_input else []

# Run Audit Button
if st.button("Run Audit"):
    if not urls:
        st.warning("Please enter at least one URL.")
    else:
        results = []

        for url in urls:
            try:
                response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract Title Tag Safely
                title_tag = soup.title.get_text(strip=True) if soup.title and soup.title.get_text(strip=True) else 'MISSING'
                title_len = len(title_tag.encode('utf-8')) if title_tag != 'MISSING' else 0

                # Extract Meta Description Safely
                meta_tag = soup.find('meta', attrs={'name': 'description'})
                meta_description = meta_tag.get('content', '').strip() if meta_tag else 'MISSING'
                meta_len = len(meta_description.encode('utf-8')) if meta_description != 'MISSING' else 0

                # Canonical Tag
                canonical_tag = soup.find('link', rel='canonical')
                canonical_url = canonical_tag.get('href', '').strip() if canonical_tag else 'MISSING'

                # H1 Tag
                h1_tag = soup.find('h1')
                h1_text = h1_tag.get_text(strip=True) if h1_tag else 'MISSING'

                # ALT Texts
                images = soup.find_all('img')
                missing_alts = [img.get('src') for img in images if not img.get('alt')]

                # Length Validations
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
                    'Meta Description': 'ERROR',
                    'H1 Tag': 'ERROR',
                    'Canonical Tag': 'ERROR',
                    'Missing ALT Images Count': 'ERROR'
                })

        # Show Results in DataFrame
        df = pd.DataFrame(results)
        st.success("Audit Complete! Download your report below.")
        st.dataframe(df)

        # Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            data=csv,
            file_name='onpage_seo_audit.csv',
            mime='text/csv'
        )
