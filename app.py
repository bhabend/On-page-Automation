import streamlit as st
from serp_api import get_serp_data
from gpt_analysis import analyze_content_gap
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="SEO Keyword & Content Gap Analyzer", layout="wide")

st.title("🔍 SEO Keyword & Content Gap Analyzer")

keyword = st.text_input("Enter Keyword", "")
target_url = st.text_input("Enter Your Website URL", "")

if st.button("Analyze") and keyword and target_url:
    with st.spinner("Fetching SERP data..."):
        serp_results = get_serp_data(keyword)

    if serp_results:
        st.subheader("📈 SERP Top 10 Results")
        for result in serp_results:
            st.markdown(f"- **{result['position']}. [{result['title']}]({result['url']})**")

        # Filter Competitors (Exclude Target URL)
        competitors = [res for res in serp_results if target_url not in res['url']][:3]
        
        st.subheader("⚔️ Top Competitors Selected for Analysis")
        for comp in competitors:
            st.markdown(f"- **{comp['position']}. [{comp['title']}]({comp['url']})**")

        def fetch_text(url):
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.content, "html.parser")
                texts = soup.stripped_strings
                return ' '.join(list(texts)[:500])
            except:
                return "Content could not be fetched."

        with st.spinner("Fetching website content..."):
            target_content = fetch_text(target_url)
            competitor_contents = [fetch_text(comp['url']) for comp in competitors]

        with st.spinner("Analyzing Content Gaps using GPT..."):
            insights = analyze_content_gap(keyword, target_content, competitor_contents)

        if insights:
            st.markdown("## 📊 Content Gap Insights")

            # Split GPT Response into Bullet Points
            sections = insights.split('\n')
            current_section = ""
            for line in sections:
                if line.strip() == "":
                    continue
                elif line.strip().endswith(':'):
                    current_section = line.strip()
                    st.markdown(f"### {current_section}")
                elif line.strip().startswith("-") or line.strip().startswith("•"):
                    st.markdown(f"{line}")
                else:
                    st.markdown(f"{line}")
        else:
            st.error("❌ GPT failed to generate insights. Please retry.")
    else:
        st.error("❌ Failed to fetch SERP data. Check API Key or quota.")
