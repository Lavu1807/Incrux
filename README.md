# 🗞️ News-Flash: The 60-Second News Summarizer

> **Automated daily news digests powered by AI. Fetch, summarize, and email in 60 seconds.**

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

## 🎯 Overview

**News-Flash** is a production-ready Python automation project that transforms raw news into actionable intelligence. Every morning, it:

1. **Fetches** the latest articles on a topic from NewsAPI
2. **Summarizes** them into 3 crisp, fact-based bullet points using OpenAI GPT
3. **Emails** a beautifully formatted digest to your inbox

Perfect for busy professionals, investors, and founders who need daily market intelligence without scrolling through 100 articles.

---

## ✨ Key Features

- ✅ **Real-time News Fetching** - Queries NewsAPI for the latest articles
- ✅ **AI-Powered Summarization** - GPT-3.5-turbo generates actionable bullet points
- ✅ **Multi-User Web Application** - Professional UI with user accounts and personalized dashboards
- ✅ **Beautiful Email Reports** - HTML-formatted emails with clickable article links
- ✅ **Fully Automated** - Schedule with Windows Task Scheduler or Linux Cron
- ✅ **Secure Credentials** - Environment variables protect API keys
- ✅ **Error Handling** - Graceful fallbacks and detailed logging
- ✅ **Modular Architecture** - Clean separation of concerns for easy maintenance

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **News Source** | NewsAPI (newsapi.org) |
| **AI Engine** | Google Gemini / OpenAI GPT |
| **Web Framework** | Flask with SQLAlchemy |
| **Database** | SQLite |
| **Authentication** | Flask-Login with password hashing |
| **Email Service** | Gmail SMTP |
| **Scheduling** | Windows Task Scheduler / Linux Cron |
| **Language** | Python 3.8+ |
| **Dependencies** | Flask, requests, python-dotenv, openai, google-generativeai |

---

## 📋 Project Structure

```
news-flash/
│
├── main.py              # Entry point, orchestrates the pipeline
├── fetch_news.py        # Phase 1: News fetching from NewsAPI
├── summarize.py         # Phase 2: AI summarization with OpenAI
├── emailer.py           # Phase 3: Email sending via SMTP
├── config.py            # Configuration and env variable management
├── .env                 # Environment variables (NEVER commit this!)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

### Data Flow Architecture

```
┌─────────────────┐
│   NewsAPI       │
│   (Topic Query) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   fetch_news.py                     │
│   - Query topic                     │
│   - Extract title, description, URL │
│   - Return clean articles list      │
└────────┬────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│   summarize.py                       │
│   - Combine articles into prompt     │
│   - Send to OpenAI GPT               │
│   - Generate 3 bullet points         │
│   - Return structured summary        │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│   emailer.py                         │
│   - Create HTML email template       │
│   - Attach summary + article links   │
│   - Send via Gmail SMTP              │
└──────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- API keys for:
  - [NewsAPI](https://newsapi.org) (free tier available)
  - [OpenAI](https://platform.openai.com/api-keys) (paid account)
  - Gmail account (for sending emails)

### 1️⃣ Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/news-flash.git
cd news-flash
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure API Keys

Create a `.env` file in the project root:

```bash
# NewsAPI Configuration
NEWS_API_KEY=your_newsapi_key_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECIPIENT=recipient@example.com

# News Topic
NEWS_TOPIC=Indian Startups
```

#### 📌 Getting Gmail App Password
1. Enable 2-Factor Authentication on your Google account
2. Go to [Google Account → App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a 16-character App Password
4. Use this password in `.env` (NOT your regular Gmail password)

### 3️⃣ Test Run

Test the complete pipeline:

```bash
# Run with default configuration
python main.py

# Test without sending email
python main.py --no-email

# Custom topic
python main.py --topic "Tesla News"

# Custom recipient
python main.py --recipient custom@example.com
```

---

## 📅 Scheduling

### Windows Task Scheduler

1. **Open Task Scheduler**
   - Press `Win + R` → Type `taskschd.msc` → Enter

2. **Create a New Task**
   - Right-click "Task Scheduler Library" → "Create Basic Task"
   - Name: `NewsFlash Daily`
   - Trigger: Daily at 8:00 AM

3. **Set Action**
   - Action: Start a program
   - Program: `C:\Program Files\Python311\python.exe`
   - Arguments: `C:\path\to\news-flash\main.py`
   - Start in: `C:\path\to\news-flash`

4. **Finish & Activate**

### Linux Cron Job

Add to your crontab:

```bash
crontab -e

# Run daily at 8:00 AM
0 8 * * * cd /path/to/news-flash && /usr/bin/python3 main.py
```

Verify cron job:
```bash
crontab -l
```

### GitHub Actions (Advanced)

Create `.github/workflows/news-flash.yml`:

```yaml
name: News-Flash Daily

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM UTC

jobs:
  news-flash:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          EMAIL_SENDER: ${{ secrets.EMAIL_SENDER }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_RECIPIENT: ${{ secrets.EMAIL_RECIPIENT }}
```

---

## 📖 Usage Guide

### Web Application (Recommended)

```bash
# Start the web server
C:/Users/HP/Desktop/news_crux/.venv/Scripts/python.exe webapp/app.py

# Open browser to http://localhost:5000
# Sign up, add topics, and view news summaries
```

### CLI Pipeline

```bash
# Run complete pipeline
python main.py
```

### Command-Line Options

```bash
# Custom topic
python main.py --topic "Cryptocurrency News"

# Test mode (no email)
python main.py --no-email

# Custom recipient
python main.py --recipient analyst@company.com

# Fetch more articles
python main.py --max-articles 20

# Combine options
python main.py --topic "AI News" --no-email --max-articles 15
```

### Programmatic Usage

```python
from fetch_news import fetch_news
from summarize import summarize_news
from emailer import send_email

# Fetch news
articles = fetch_news(topic="Stock Market", max_articles=10)

# Summarize
summary = summarize_news(articles)
print(summary)

# Send email
send_email(
    subject="📰 Market Update",
    summary=summary,
    articles=articles,
    recipient="investor@example.com"
)
```

---

## 📧 Email Output Example

**Subject:** 🗞️ News-Flash | Indian Startups

**Body Preview:**
```
📌 KEY HIGHLIGHTS:

• Indian fintech startups raised $120M this week, led by Series B rounds from 
  Sequoia Capital and Accel Partners, targeting underbanked populations

• Government announced new incentives for early-stage SaaS companies, including 
  ₹500 Cr fund allocation and faster regulatory approval

• Tech layoffs declined by 18% YoY, signaling market stabilization with focus 
  shifting to profitability and sustainable growth

📚 FULL ARTICLES:
- "India's Startup Funding Hits $15B in 2023..." - TechCrunch
- "GST incentives for SaaS startups..." - LiveMint
- "Tech Job Market Stabilizes..." - YourStory
```

---

## 🔒 Security Best Practices

✅ **What We Do Right:**
- All API keys stored in `.env` (never in code)
- `.env` added to `.gitignore` to prevent accidental commits
- Credentials validated at runtime
- Error messages don't leak sensitive information

✅ **What You Should Do:**
- Rotate API keys periodically
- Use Gmail App Passwords, not regular passwords
- Never commit `.env` to version control
- Store credentials securely (HashiCorp Vault, AWS Secrets Manager in production)

---

## 📊 Phases & Implementation

### Phase 0: ✅ Project Planning
- Modular architecture designed
- Responsibilities defined per file
- Data flow documented

### Phase 1: ✅ Fetch News
- **File:** `fetch_news.py`
- Queries NewsAPI for latest articles
- Returns structured data: title, description, URL, source
- Error handling for API failures

### Phase 2: ✅ AI Summarization
- **File:** `summarize.py`
- OpenAI GPT-3.5-turbo for summarization
- Enforces 3 bullet-point format
- Optimized prompt for factual, concise output

### Phase 3: ✅ Email Automation
- **File:** `emailer.py`
- Beautiful HTML email template
- SMTP via Gmail
- Article links included

### Phase 4: ✅ Scheduling
- **File:** `main.py`
- Windows Task Scheduler guide
- Linux Cron configuration
- GitHub Actions example

### Phase 5: ✅ Security & Config
- **File:** `config.py`, `.env`
- Environment variable management
- Validation and error handling
- No hardcoded secrets

### Phase 6: ✅ Polish
- **File:** `README.md`
- Professional documentation
- Setup instructions
- Resume-ready project

---

## 🏆 Resume Impact

This project demonstrates:

1. **API Integration** - Real-world integration with multiple APIs (NewsAPI, OpenAI, SMTP)
2. **Prompt Engineering** - Crafting effective prompts for consistent, high-quality outputs
3. **System Design** - Modular architecture with separation of concerns
4. **Error Handling** - Graceful degradation and informative error messages
5. **Automation** - Scheduling and background execution
6. **Security** - Best practices for credential management
7. **Full Stack** - Data pipeline from API → Processing → Output
8. **Production Readiness** - Logging, validation, and documentation

### Talking Points for Interviews:
- "Built a fully automated news processing pipeline using OpenAI GPT"
- "Designed modular Python architecture for scalability"
- "Implemented secure credential management with environment variables"
- "Integrated with multiple third-party APIs (NewsAPI, OpenAI, Gmail)"
- "Automated daily execution using Task Scheduler/Cron"
- "Created HTML email templates for professional reporting"

---

## 🐛 Troubleshooting

### Issue: "Invalid API key" error

**Solution:**
- Verify your API keys in `.env`
- For NewsAPI: Check at [newsapi.org/account](https://newsapi.org/account)
- For OpenAI: Check at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Issue: Email not sending

**Solution:**
- For Gmail: Use App Password, not your regular password
- Enable "Less secure apps" (if 2FA not enabled)
- Check that EMAIL_SENDER matches Gmail account
- Verify firewall isn't blocking SMTP port 587

### Issue: No articles found

**Solution:**
- NewsAPI free tier has limits. Check usage at [newsapi.org/account](https://newsapi.org/account)
- Try a more common topic (e.g., "Technology", "Business")
- Increase `max_articles` parameter

### Issue: Rate limit exceeded

**Solution:**
- OpenAI: Upgrade plan or reduce request frequency
- NewsAPI: Wait 24 hours or upgrade plan
- Implement caching to reduce duplicate requests

---

## 📈 Future Improvements

- [ ] Multi-topic support (fetch news on 3+ topics)
- [ ] Database storage (SQLite) for article history
- [ ] Web dashboard to view past digests
- [ ] Customizable summary length
- [ ] Topic-specific prompts (finance, tech, healthcare)
- [ ] Newsletter format with archives
- [ ] Slack/Teams integration
- [ ] Multiple recipient support
- [ ] Cloud deployment (AWS Lambda, Google Cloud)
- [ ] Advanced caching to reduce API costs

---

## 📝 License

MIT License - feel free to use this for your portfolio!

---

## 🙌 Credits

- **NewsAPI** - Real-time news data
- **OpenAI** - GPT-3.5-turbo API
- **Python Community** - Excellent libraries

---

## 📞 Support

Found a bug or have suggestions? Open an issue or contact me!

---

**Made with ❤️ by [Your Name]**

*P.S. - This project went from zero to production in one afternoon. Imagine what we can build together.* 🚀
