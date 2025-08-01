import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_content_gap(keyword, target_content, competitor_contents):
    prompt = f"""
You are an expert SEO Content Analyst.

Task: Analyze the content gap for the keyword: "{keyword}".
Provide the following insights in detailed bullet points:
1. Keyword Usage Comparison.
2. LSI/NLP Terms missing from My Website.
3. Topic and Structural Gaps.
4. Actionable Recommendations to improve ranking.

--- My Website Content ---
{target_content}

--- Competitor 1 Content ---
{competitor_contents[0]}

--- Competitor 2 Content ---
{competitor_contents[1]}

--- Competitor 3 Content ---
{competitor_contents[2]}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
