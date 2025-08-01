import streamlit as st
from serp_api import get_serp_data
from gpt_analysis import analyze_content_gap
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="SEO Keyword & Content Gap Analyzer", layout="wide")

st.title("🔍 SEO Keyword & Content Gap Analyzer")

# Input Section
keyword = st.text_input("Enter Keyword", "")
target_url = st.text_input("Enter Your Website URL", "")

if st.button("Analyze") and keyword and target_url:
    with st.spinner("Fetching SERP data..."):
        serp_results = get_serp_data(keyword)

    if serp_results:
        st.subheader("📈 SERP Top 10 Results:")
        for result in serp_results:
            st.markdown(f"{result['position']}. [{result['title']}]({result['url']})")

        # Identify top 3 competitors (excluding your site)
        competitors = [res for res in serp_results if target_url not in res['url']][:3]
        st.subheader("⚔️ Top Competitors:")
        for comp in competitors:
            st.markdown(f"{comp['position']}. [{comp['title']}]({comp['url']})")

        # Scrape content for analysis
        def fetch_text_from_url(url):
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.content, "html.parser")
                texts = soup.stripped_strings
                return ' '.join(list(texts)[:500])
            except:
                return ""

        with st.spinner("Fetching website content..."):
            target_content = fetch_text_from_url(target_url)
            competitor_contents = [fetch_text_from_url(comp['url']) for comp in competitors]

        # Analyze with GPT
        with st.spinner("Analyzing content gaps with GPT..."):
            insights = analyze_content_gap(keyword, target_content, competitor_contents)

        if insights:
            st.markdown("### 📊 Content Gap Insights")
            st.markdown(insights)
        else:
            st.error("❌ No insights generated. Please check inputs or try again.")
    else:
        st.error("❌ Failed to fetch SERP data. Check API Key or quota.")
