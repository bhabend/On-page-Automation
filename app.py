import streamlit as st
import pandas as pd
from playwright_crawler import fetch_rendered_html
from seo_audit import audit_seo
from psi_api import get_pagespeed_data
from utils import score_page

st.set_page_config(page_title="SEO Audit Tool", layout="wide")

st.title("On-Page SEO Audit Tool")

urls_input = st.text_area("Enter URLs (one per line)", height=200)
start = st.button("Run Audit")

if start and urls_input:
    urls = [u.strip() for u in urls_input.strip().split("\n") if u.strip()]
    results = []

    for url in urls:
        st.write(f"Auditing: {url}")
        html = fetch_rendered_html(url)
        if not html:
            continue

        seo_data = audit_seo(html, url)
        psi_data = get_pagespeed_data(url)
        combined = {**seo_data, **psi_data}
        combined["Score"] = score_page(combined)
        combined["URL"] = url
        results.append(combined)

    df = pd.DataFrame(results)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "seo_audit_results.csv", "text/csv")
