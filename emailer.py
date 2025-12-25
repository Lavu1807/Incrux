"""
Phase 3: Email Automation
This module handles sending formatted email notifications with news summaries.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
from config import Config


def create_email_body(summary: str, articles: List[Dict[str, str]]) -> tuple:
    """
    Create HTML and plain text email body.
    
    Args:
        summary (str): The AI-generated summary with bullet points.
        articles (List[Dict]): List of articles for links.
    
    Returns:
        tuple: (html_body, text_body) for email content.
    """
    
    # Generate article links
    article_links = ""
    for article in articles:
        title = article.get("title", "Untitled")
        url = article.get("url", "#")
        source = article.get("source", "Unknown")
        article_links += f'<li><a href="{url}">{title}</a><br><small>{source}</small></li>\n'
    
    # HTML email body
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto;">
                <header style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center;">
                    <h1 style="margin: 0; font-size: 24px;">🗞️ News-Flash</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Your 60-Second News Summary</p>
                </header>
                
                <section style="padding: 20px; background: #f9f9f9;">
                    <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">
                        📰 {Config.NEWS_TOPIC}
                    </h2>
                    <p style="color: #666; font-size: 14px;">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </section>
                
                <section style="padding: 20px;">
                    <h3 style="color: #333; margin-top: 0;">📌 Key Highlights</h3>
                    <div style="background: #f0f4ff; padding: 15px; border-left: 4px solid #667eea; border-radius: 4px;">
                        {summary.replace(chr(10), '<br>')}
                    </div>
                </section>
                
                <section style="padding: 20px; background: #f9f9f9;">
                    <h3 style="color: #333;">📚 Full Articles</h3>
                    <ul style="list-style-type: none; padding: 0;">
                        {article_links}
                    </ul>
                </section>
                
                <footer style="background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; font-size: 12px;">
                    <p style="margin: 0;">Powered by News-Flash • NewsAPI • OpenAI GPT</p>
                    <p style="margin: 5px 0 0 0; opacity: 0.8;">🚀 Your Daily Briefing in 60 Seconds</p>
                </footer>
            </div>
        </body>
    </html>
    """
    
    # Plain text email body
    text_body = f"""
News-Flash: Your 60-Second News Summary
========================================

📰 {Config.NEWS_TOPIC}
Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

📌 KEY HIGHLIGHTS:
{summary}

📚 FULL ARTICLES:
{chr(10).join([f"- {article.get('title')} ({article.get('source')})\n  {article.get('url')}" for article in articles])}

========================================
Powered by News-Flash • NewsAPI • OpenAI GPT
🚀 Your Daily Briefing in 60 Seconds
    """
    
    return html_body, text_body.strip()


def send_email(subject: str, summary: str, articles: List[Dict[str, str]], 
               recipient: str = None) -> bool:
    """
    Send formatted email with news summary.
    
    Args:
        subject (str): Email subject line.
        summary (str): The AI-generated summary.
        articles (List[Dict]): List of articles.
        recipient (str): Email recipient. Defaults to EMAIL_RECIPIENT from config.
    
    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    
    recipient = recipient or Config.EMAIL_RECIPIENT
    
    try:
        # Create email message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = Config.EMAIL_SENDER
        message["To"] = recipient
        
        # Create email body
        html_body, text_body = create_email_body(summary, articles)
        
        # Attach both text and HTML versions
        message.attach(MIMEText(text_body, "plain"))
        message.attach(MIMEText(html_body, "html"))
        
        print("📧 Connecting to email server...")
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()  # Upgrade connection to secure
            
            print("🔐 Authenticating...")
            server.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
            
            print(f"📤 Sending email to {recipient}...")
            server.sendmail(Config.EMAIL_SENDER, recipient, message.as_string())
        
        print("✓ Email sent successfully!")
        return True
    
    except smtplib.SMTPAuthenticationError:
        print("✗ Authentication failed!")
        print("  → Check your EMAIL and EMAIL_PASSWORD in .env")
        print("  → For Gmail: Use an App Password, not your regular password")
        print("  → Enable 2FA and generate an App Password at: https://myaccount.google.com/apppasswords")
        return False
    
    except smtplib.SMTPException as e:
        print(f"✗ SMTP error: {str(e)}")
        return False
    
    except Exception as e:
        print(f"✗ Error sending email: {str(e)}")
        return False


if __name__ == "__main__":
    # Test email functionality
    from fetch_news import fetch_news
    from summarize import summarize_news
    
    print("Testing email functionality...\n")
    
    # Fetch and summarize news
    articles = fetch_news(topic="Indian Startups", max_articles=5)
    
    if articles:
        summary = summarize_news(articles)
        
        # Send email
        send_email(
            subject="🗞️ News-Flash | Indian Startups",
            summary=summary,
            articles=articles
        )
    else:
        print("No articles to send.")
