import openai

OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'  # <-- Replace with your actual OpenAI API key
openai.api_key = OPENAI_API_KEY

def analyze_content_gap(keyword, target_content, competitor_contents):
    prompt = f"""
    Analyze the SEO content gap for the keyword: "{keyword}".

    My Website Content:
    {target_content}

    Competitor 1 Content:
    {competitor_contents[0]}

    Competitor 2 Content:
    {competitor_contents[1]}

    Competitor 3 Content:
    {competitor_contents[2]}

    Provide:
    1. Keyword Usage Comparison.
    2. LSI/NLP Terms that my content is missing.
    3. Content Topic Gaps.
    4. Actionable Suggestions to improve ranking.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
