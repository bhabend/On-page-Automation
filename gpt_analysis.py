import os
from openai import OpenAI

# Load API Key from Environment Variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_content_gap(keyword, target_content, competitor_contents):
    prompt = f"""
    You are an SEO Content Analyst. Analyze the SEO content gap for the keyword: "{keyword}".

    My Website Content:
    {target_content}

    Competitor 1 Content:
    {competitor_contents[0]}

    Competitor 2 Content:
    {competitor_contents[1]}

    Competitor 3 Content:
    {competitor_contents[2]}

    Provide the following insights:
    1. Keyword Usage Comparison.
    2. LSI/NLP Terms that my content is missing.
    3. Content Topic Gaps.
    4. Actionable Suggestions to improve ranking.
    """
    # <-- Correctly closed the t
