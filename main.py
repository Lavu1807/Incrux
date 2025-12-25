"""
Phase 4 & Main Entry Point: News-Flash
Complete pipeline: Fetch → Summarize → Email
"""

import sys
import argparse
from datetime import datetime
from config import Config
from fetch_news import fetch_news
from summarize import summarize_news
from emailer import send_email


def run_pipeline(topic: str = None, send_email_flag: bool = True, 
                 recipient: str = None, max_articles: int = None) -> bool:
    """
    Execute the complete News-Flash pipeline:
    1. Fetch latest news articles
    2. Summarize using AI
    3. Send email notification
    
    Args:
        topic (str): News topic to search. Defaults to NEWS_TOPIC from config.
        send_email_flag (bool): Whether to send email. Default is True.
        recipient (str): Email recipient. Defaults to EMAIL_RECIPIENT from config.
        max_articles (int): Maximum articles to fetch. Defaults to MAX_ARTICLES from config.
    
    Returns:
        bool: True if pipeline completed successfully, False otherwise.
    """
    
    topic = topic or Config.NEWS_TOPIC
    max_articles = max_articles or Config.MAX_ARTICLES
    recipient = recipient or Config.EMAIL_RECIPIENT
    
    print("\n" + "=" * 60)
    print("🚀 NEWS-FLASH: 60-Second News Summarizer")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📰 Topic: {topic}")
    print("=" * 60 + "\n")
    
    try:
        # Phase 1: Fetch News
        print("[PHASE 1] Fetching News Articles...")
        print("-" * 60)
        articles = fetch_news(topic=topic, max_articles=max_articles)
        
        if not articles:
            print("\n✗ Pipeline failed: No articles found.")
            return False
        
        print(f"\n✓ Phase 1 Complete: {len(articles)} articles fetched\n")
        
        # Phase 2: Summarize
        print("[PHASE 2] Generating AI Summary...")
        print("-" * 60)
        summary = summarize_news(articles)
        
        if not summary or summary == "No articles to summarize.":
            print("\n✗ Pipeline failed: Summary generation failed.")
            return False
        
        print("\n✓ Phase 2 Complete: Summary generated\n")
        print("Summary Preview:")
        print("-" * 60)
        print(summary)
        print("-" * 60 + "\n")
        
        # Phase 3: Email (Optional)
        if send_email_flag:
            print("[PHASE 3] Sending Email Notification...")
            print("-" * 60)
            
            subject = f"🗞️ News-Flash | {topic}"
            success = send_email(subject, summary, articles, recipient)
            
            if success:
                print(f"\n✓ Phase 3 Complete: Email sent to {recipient}\n")
            else:
                print(f"\n✗ Phase 3 Failed: Email not sent\n")
                return False
        else:
            print("[PHASE 3] Skipped: Email notification disabled\n")
        
        # Success
        print("=" * 60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")
        
        return True
    
    except Exception as e:
        print(f"\n✗ PIPELINE ERROR: {str(e)}")
        print("=" * 60 + "\n")
        return False


def main():
    """Command-line entry point for News-Flash."""
    
    parser = argparse.ArgumentParser(
        description="News-Flash: 60-Second AI News Summarizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default configuration
  python main.py
  
  # Run with custom topic
  python main.py --topic "Tesla News"
  
  # Run without sending email (test mode)
  python main.py --no-email
  
  # Run with custom recipient
  python main.py --recipient custom@example.com
        """
    )
    
    parser.add_argument(
        "--topic",
        type=str,
        help="News topic to search (default: from .env)"
    )
    
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Run without sending email (testing mode)"
    )
    
    parser.add_argument(
        "--recipient",
        type=str,
        help="Email recipient (default: from .env)"
    )
    
    parser.add_argument(
        "--max-articles",
        type=int,
        help="Maximum articles to fetch (default: 10)"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease update your .env file with the required API keys.")
        sys.exit(1)
    
    # Run the pipeline
    success = run_pipeline(
        topic=args.topic,
        send_email_flag=not args.no_email,
        recipient=args.recipient,
        max_articles=args.max_articles
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
