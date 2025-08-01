import streamlit as st
from serp_api import get_serp_data
from content_extractor import extract_content
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

            # Extract Your Website Content
            with st.spinner("Extracting your website content..."):
                target_content = extract_content(website_url)
            
            st.subheader("📝 Your Website Content Preview")
            st.write(target_content[:500] + " ...")  # Show first 500 characters

            # Extract Competitor Contents
            st.subheader("📰 Competitor Content Extracts")
            competitor_contents = []
            for idx, comp in enumerate(serp_results[:3]):
                with st.spinner(f"Fetching Competitor {idx+1} Content..."):
                    comp_content = extract_content(comp['url'])
                    competitor_contents.append(comp_content)
                    st.markdown(f"**Competitor {idx+1}: [{comp['title']}]({comp['url']})**")
                    st.write(comp_content[:500] + " ...")  # Show first 500 characters

            # --- MOCKED GPT RESPONSE ---
            st.subheader("🧠 GPT-Powered SEO Gap Insights")
            demo_insights = f"""
            - Your content lacks coverage on recent **NLP/LSI terms** like "on-chain metrics" and "Layer 2 scaling solutions".
            - Competitors are integrating more visual data (infographics, charts).
            - Suggested Action: Add a section on 'Ethereum's Future Roadmap', optimize H2 tags with variants of '{keyword}', and increase internal linking.
            """
            st.info(demo_insights)

            # CSV Export Button
            csv_data = pd.DataFrame([{"Keyword": keyword, "Insights": demo_insights}])
            csv = csv_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Insights as CSV",
                data=csv,
                file_name=f"{keyword}_SEO_Insights.csv",
                mime='text/csv',
            )
