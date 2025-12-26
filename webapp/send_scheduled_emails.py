"""
Scheduled Email Sender for News-Flash
Sends personalized news summaries to users at their preferred time.
Run this script every hour via Task Scheduler/Cron.
"""

import sys
import os

# Set working directory to the webapp directory to ensure DB is found
os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
from app import app, db, User, NewsPreference
from fetch_news import fetch_news
from summarize import summarize_news
from emailer import send_email

def send_user_emails():
    """Send emails to users whose preferred time matches current hour."""
    
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        current_time = datetime.now().strftime('%H:%M')
        current_hour = datetime.now().strftime('%H')
        
        print(f"[{datetime.now()}] Checking for emails to send at {current_time}")
        
        # Find users whose preferred time hour matches current hour and email is enabled
        users = User.query.filter(
            User.email_enabled == True,
            User.preferred_email_time.startswith(current_hour)
        ).all()
        
        if not users:
            print(f"No users scheduled for {current_hour}:00")
            return
        
        print(f"Found {len(users)} users to send emails to")
        
        for user in users:
            try:
                print(f"\n--- Processing user: {user.username} ({user.email}) ---")
                
                # Get user's topics
                if not user.preferences:
                    print(f"  No topics set for {user.username}, skipping")
                    continue
                
                # Combine all topics or send separate emails per topic
                all_articles = []
                all_summaries = []
                
                for pref in user.preferences:
                    print(f"  Fetching news for topic: {pref.topic}")
                    articles = fetch_news(pref.topic, max_articles=pref.max_articles)
                    
                    if articles:
                        print(f"  Found {len(articles)} articles for {pref.topic}")
                        summary = summarize_news(articles)
                        
                        all_articles.extend(articles)
                        all_summaries.append(f"<h3>{pref.topic}</h3>{summary}")
                
                if not all_articles:
                    print(f"  No articles found for {user.username}, skipping email")
                    continue
                
                # Create combined summary
                combined_summary = "<br><br>".join(all_summaries)
                
                # Create email subject
                topics_str = ", ".join([p.topic for p in user.preferences[:3]])
                if len(user.preferences) > 3:
                    topics_str += "..."
                subject = f"News-Flash Daily Summary | {topics_str}"
                
                # Send email
                print(f"  Sending email to {user.email}")
                send_email(user.email, subject, combined_summary, all_articles)
                print(f"  ✓ Email sent successfully to {user.username}")
                
            except Exception as e:
                print(f"  ✗ Error sending email to {user.username}: {str(e)}")
                continue
        
        print(f"\n[{datetime.now()}] Email sending complete")

if __name__ == "__main__":
    send_user_emails()
