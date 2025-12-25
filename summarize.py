"""
Phase 2: AI Summarization
This module handles AI-powered news summarization using OpenAI API.
"""

from typing import List, Dict
from config import Config
from openai import OpenAI


def format_articles_for_prompt(articles: List[Dict[str, str]]) -> str:
    """
    Format articles into a readable text block for the GPT prompt.
    
    Args:
        articles (List[Dict]): List of articles with title, description, url.
    
    Returns:
        str: Formatted articles text.
    """
    if not articles:
        return "No articles available."
    
    formatted = "NEWS ARTICLES:\n" + "=" * 50 + "\n\n"
    
    for idx, article in enumerate(articles, 1):
        formatted += f"Article {idx}:\n"
        formatted += f"Title: {article.get('title', 'N/A')}\n"
        formatted += f"Description: {article.get('description', 'N/A')}\n"
        formatted += f"Source: {article.get('source', 'N/A')}\n"
        formatted += f"URL: {article.get('url', 'N/A')}\n"
        formatted += "-" * 50 + "\n\n"
    
    return formatted


def summarize_news(articles: List[Dict[str, str]]) -> str:
    """
    Summarize news articles into 3 concise bullet points using the selected provider.
    Provider options: OPENAI (default) or GEMINI. Falls back to local summary on error.
    """

    if not articles:
        return "No articles to summarize."

    articles_text = format_articles_for_prompt(articles)

    system_prompt = """You are a financial news analyst specializing in technology and startup ecosystems.
Your task is to synthesize multiple news articles into concise, factual bullet points.
Focus on business impact, market trends, and key developments.
Be objective and neutral in tone."""

    user_prompt = f"""{articles_text}

Based on the above articles, summarize the key news into exactly 3 concise bullet points.
Each bullet should:
- Be 1-2 sentences maximum
- Highlight the most important development or trend
- Be readable in under 60 seconds total
- Avoid repetition and be factually accurate
- Include specific numbers or names when available

Format your response as:
• [Bullet 1]
• [Bullet 2]
• [Bullet 3]"""

    provider = (Config.AI_PROVIDER or "OPENAI").upper()

    if provider == "GEMINI":
        return _summarize_gemini(system_prompt, user_prompt, articles)
    # Default to OPENAI
    return _summarize_openai(system_prompt, user_prompt, articles)


def _summarize_openai(system_prompt: str, user_prompt: str, articles: List[Dict[str, str]]) -> str:
    """Call OpenAI Chat Completions API and fall back on errors."""
    try:
        print("🧠 Generating AI summary (OpenAI)...")

        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300,
            top_p=1.0
        )

        summary = response.choices[0].message.content.strip()
        print("✓ Summary generated successfully")
        return summary

    except Exception as e:
        print(f"✗ Error generating summary (OpenAI): {str(e)}")
        if "401" in str(e) or "Unauthorized" in str(e):
            print("  → Invalid OpenAI API key. Please check OPENAI_API_KEY in .env")
        elif "429" in str(e) or "rate limit" in str(e).lower() or "insufficient_quota" in str(e).lower():
            print("  → Rate limit/quota exceeded. Using local fallback summary.")
        else:
            print("  → Falling back to local summary due to an unexpected error.")
        return _fallback_summary(articles)


def _summarize_gemini(system_prompt: str, user_prompt: str, articles: List[Dict[str, str]]) -> str:
    """Call Gemini API and fall back on errors."""
    if not Config.GEMINI_API_KEY:
        print("✗ Gemini API key missing. Falling back to local summary.")
        return _fallback_summary(articles)

    try:
        print("🧠 Generating AI summary (Gemini)...")
        import google.generativeai as genai

        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel(Config.GEMINI_MODEL)
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")

        summary = (response.text or "").strip()
        if not summary:
            print("✗ Empty response from Gemini. Falling back to local summary.")
            return _fallback_summary(articles)

        print("✓ Summary generated successfully")
        return summary

    except Exception as e:
        print(f"✗ Error generating summary (Gemini): {str(e)}")
        if "permission" in str(e).lower() or "invalid" in str(e).lower():
            print("  → Check GEMINI_API_KEY and GEMINI_MODEL in .env")
        elif "quota" in str(e).lower() or "rate" in str(e).lower():
            print("  → Rate limit/quota exceeded. Using local fallback summary.")
        else:
            print("  → Falling back to local summary due to an unexpected error.")
        return _fallback_summary(articles)


def _fallback_summary(articles: List[Dict[str, str]]) -> str:
    """
    Local fallback summarization when OpenAI API is unavailable.
    Produces exactly 3 concise bullets from the top articles' titles/descriptions.

    Args:
        articles (List[Dict]): List of articles with title/description.

    Returns:
        str: 3 bullet points as a string.
    """
    if not articles:
        return "No articles to summarize."

    def clean(text: str) -> str:
        if not text:
            return ""
        t = text.replace("\n", " ").strip()
        return t

    bullets = []
    for a in articles[:3]:
        title = clean(a.get("title", ""))
        desc = clean(a.get("description", ""))
        if desc:
            snippet = desc[:180]
        else:
            snippet = title[:180]
        if title:
            bullet = f"• {title} — {snippet}"
        else:
            bullet = f"• {snippet}"
        bullets.append(bullet)

    # Ensure exactly 3 bullets (pad or trim)
    while len(bullets) < 3:
        bullets.append("• Additional update pending due to API limits.")
    bullets = bullets[:3]

    return "\n".join(bullets)


def get_article_links(articles: List[Dict[str, str]]) -> str:
    """
    Generate formatted article links for email inclusion.
    
    Args:
        articles (List[Dict]): List of articles with title and url.
    
    Returns:
        str: Formatted links in HTML format.
    """
    if not articles:
        return ""
    
    html = "<h3>📚 Read Full Articles:</h3>\n<ul>\n"
    
    for article in articles:
        title = article.get("title", "Untitled")
        url = article.get("url", "#")
        source = article.get("source", "Unknown")
        html += f'<li><a href="{url}">{title}</a> - {source}</li>\n'
    
    html += "</ul>"
    return html


if __name__ == "__main__":
    # Test summarization with sample articles
    from fetch_news import fetch_news
    
    articles = fetch_news(topic="Indian Startups", max_articles=5)
    
    if articles:
        summary = summarize_news(articles)
        print("\n📊 Generated Summary:\n")
        print(summary)
        print("\n" + "=" * 50)
        
        links = get_article_links(articles)
        print("\nArticle Links HTML:")
        print(links)
