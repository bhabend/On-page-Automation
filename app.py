import streamlit as st
from serp_api import get_serp_data
from content_extractor import fetch_page_content
from gpt_analysis import analyze_content_gap

st.title("SEO Keyword & Content Gap Analyzer")

keyword = st.text_input("Enter Keyword")
target_url = st.text_input("Enter Your Website URL")

if st.button("Analyze"):
    with st.spinner("Fetching SERP Data..."):
        serp_data = get_serp_data(keyword)
        st.write("SERP Top 10 Results:", serp_data)

    competitors = [site for site in serp_data if target_url not in site['url']][:3]
    st.write("Top Competitors:", competitors)

    with st.spinner("Fetching Competitor Content..."):
        target_content = fetch_page_content(target_url)
        competitor_contents = [fetch_page_content(c['url']) for c in competitors]

    with st.spinner("Analyzing Content Gap using AI..."):
        insights = analyze_content_gap(keyword, target_content, competitor_contents)

    st.subheader("Content Gap Insights")
    st.write(insights)
