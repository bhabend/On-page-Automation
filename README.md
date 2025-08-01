# SEO Keyword & Content Gap Analyzer

A simple Streamlit app to:
- Analyze keyword rankings.
- Compare your website’s content against top competitors.
- Get GPT-powered SEO gap insights and improvement suggestions.

## 🛠️ Features
- Fetch SERP Top 10 results using SerpAPI.
- Extract content from competitor websites.
- Analyze Keyword Gaps, NLP/LSI Terms, and Topic Gaps using GPT.
- Actionable content improvement recommendations.

## 🚀 Setup Instructions

### 1. Environment Variables
Add the following environment variables in your Render/GitHub project settings:
- `SERPAPI_KEY` → Your SerpAPI Key.
- `OPENAI_API_KEY` → Your OpenAI API Key.

### 2. Deploy on Render.com
- Connect your GitHub repository.
- Deploy the app using **Manual Deploy → Clear Cache & Deploy Latest Commit**.
- Render will automatically detect `requirements.txt` and install dependencies.

### 3. Run Locally (Optional)
If you want to test locally on your machine:
```bash
pip install -r requirements.txt
streamlit run app.py
