import streamlit as st
from serp_api import get_serp_data
from content_extractor import extract_content
from gpt_analysis import analyze_content_gap
import pandas as pd

st.set_page_config(page_title="SEO Keyword & Content Gap Analyzer", layout="wide")

st.title("🔍 SEO Keyword & Content Gap Analyzer")

# --- Input Form ---
with st.form("seo_form"):
    keyword = st.text_input("Enter Keyword", placeholder="e.g., Ethereum news")
    website_url = st.text_input("Enter Your Website URL", placeholder="https://example.com/")
    submit_button = st.form_submit_button("Analyze")

if submit_button:
    if not keyword or not website_url:
        st.error("Please enter both a keyword and your website URL.")
    else:
        with st.spinner("Fetching SERP results..."):
            serp_results = get_serp_data(keyword)
        
        if not serp_results:
            st.error("Failed to fetch SERP data. Please check your API Key or quota.")
        else:
            # Display SERP Results
            st.subheader(f"📈 SERP Results Found: {len(serp_results)}")
            for result in serp_results:
                st.markdown(f"**{result['position']}. [{result['title']}]({result['url']})**")

            # Extract Contents
            with st.spinner("Extracting website and competitor content..."):
                target_content = extract_content(website_url)
                competitor_contents = []
                for comp in serp_results[:3]:
                    comp_content = extract_content(comp['url'])
                    competitor_contents.append(comp_content)

            # Analyze Content Gap
            with st.spinner("Analyzing content gap with GPT..."):
                insights = analyze_content_gap(keyword, target_content, competitor_contents)

            # Display Insights
            if insights:
                st.markdown("---")
                st.subheader("🧠 GPT-Powered SEO Gap Insights")
                st.markdown(f"✅ **Keyword:** `{keyword}`")
                st.markdown("### 🔎 Analysis & Recommendations")
                st.info(insights)

                # CSV Export Button
                csv_data = pd.DataFrame([{"Keyword": keyword, "Insights": insights}])
                csv = csv_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Insights as CSV",
                    data=csv,
                    file_name=f"{keyword}_SEO_Insights.csv",
                    mime='text/csv',
                )
            else:
                st.error("Content gap analysis returned no insights. Please retry.")
