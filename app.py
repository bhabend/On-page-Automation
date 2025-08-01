import streamlit as st
from crawler import fetch_page_data

st.set_page_config(page_title="SEO Audit Tool", layout="wide")

st.title("🔍 On-Page SEO Audit Tool")
st.markdown("Enter a webpage URL to perform a basic SEO audit.")

url = st.text_input("Enter URL:", "https://example.com")

if st.button("Run Audit"):
    if not url.startswith("http"):
        st.warning("Please enter a valid URL including http/https.")
    else:
        with st.spinner("Fetching page data..."):
            result = fetch_page_data(url)

        if result.get("error"):
            st.error(f"Error fetching page: {result['error']}")
        else:
            st.subheader("✅ Audit Summary")
            st.markdown(f"**Title:** {result['title']}")
            st.markdown(f"**Meta Description:** {result['meta_description']}")
            st.markdown(f"**Canonical URL:** {result['canonical_url']}")
            st.markdown(f"**Word Count:** {result['word_count']}")
            st.markdown(f"**Image Count:** {result['image_count']}")
            st.markdown(f"**Images Missing Alt:** {len(result['images_missing_alt'])}")
            st.markdown(f"**Internal Links:** {len(result['internal_links'])}")
            st.markdown(f"**External Links:** {len(result['external_links'])}")

            st.subheader("🗂️ Headings Overview")
            for tag, tags_list in result['headings'].items():
                st.markdown(f"**{tag.upper()} ({len(tags_list)}):**")
                for t in tags_list:
                    st.markdown(f"- {t}")
