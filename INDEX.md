# 📚 News-Flash Documentation Index

Welcome to News-Flash! Here's where to find everything.

---

## 🎯 Start Here

**New to the project?** Follow this path:

1. **[README.md](README.md)** ← Start here! Overview, features, architecture
2. **[SETUP.md](SETUP.md)** ← Follow the 15-minute setup guide
3. **[EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md)** ← See what the output looks like

---

## 📖 Documentation Files

### For Getting Started
- **[README.md](README.md)** - Complete project overview
  - What the project does
  - Tech stack
  - Features and benefits
  - Installation instructions
  - Basic usage

- **[SETUP.md](SETUP.md)** - Step-by-step setup guide
  - Getting API keys
  - Environment setup
  - Testing your installation
  - Troubleshooting

### For Running & Scheduling
- **[SCHEDULING.md](SCHEDULING.md)** - How to automate
  - Windows Task Scheduler (GUI + PowerShell)
  - Linux Cron jobs
  - macOS LaunchAgent
  - GitHub Actions
  - Monitoring and logging

### For Examples & Reference
- **[EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md)** - See actual output
  - Console output example
  - Email output example
  - What to expect

---

## 💻 Code Files

### Web Application
1. **[webapp/app.py](webapp/app.py)** - Flask web application (RECOMMENDED)
   - Multi-user authentication system
   - Personal dashboards
   - Real-time news fetching
   - SQLite database integration

### Core Pipeline
1. **[main.py](main.py)** - CLI entry point
   - Orchestrates the complete pipeline
   - Command-line argument handling
   - Configuration validation
   - Execution logging

2. **[config.py](config.py)** - Configuration management
   - Loads environment variables
   - Validates required settings
   - Central configuration class

3. **[fetch_news.py](fetch_news.py)** - PHASE 1
   - Fetches articles from NewsAPI
   - Cleans and structures data
   - Error handling

4. **[summarize.py](summarize.py)** - PHASE 2
   - AI summarization using OpenAI
   - Prompt engineering
   - 3-bullet point format

5. **[emailer.py](emailer.py)** - PHASE 3
   - Sends formatted emails
   - HTML templates
   - Gmail SMTP integration

### Configuration Files
- **[.env](.env)** - API keys and credentials
  - Store your secrets here
  - Never commit to Git
  - `.gitignore` protects it

- **[requirements.txt](requirements.txt)** - Python dependencies
  - requests
  - python-dotenv
  - openai

- **[.gitignore](.gitignore)** - Git ignore rules
  - Protects `.env`
  - Excludes Python cache
  - Excludes IDE files

---

## 🚀 Quick Commands

### First Time Setup
```bash
python -m venv venv          # Create virtual environment
venv\Scripts\activate        # Activate (Windows)
pip install -r requirements.txt  # Install dependencies
```

### Fill in Your API Keys
Edit `.env` file:
```
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_key
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Run the Project
```bash
python main.py               # Full pipeline with email
python main.py --no-email    # Test mode (no email)
python main.py --help        # View all options
```

### Test Individual Components
```bash
python config.py             # Validate configuration
python fetch_news.py         # Test news fetching
python summarize.py          # Test summarization
python emailer.py            # Test email
```

---

## 📋 File-by-File Guide

### main.py
**Purpose:** Run this file to execute the complete pipeline

**What it does:**
- Validates configuration
- Calls fetch_news()
- Calls summarize_news()
- Calls send_email()
- Handles errors gracefully

**Usage:**
```bash
python main.py [--topic "..."] [--no-email] [--recipient "..."] [--max-articles N]
```

---

### config.py
**Purpose:** Centralized configuration management

**Key class:** `Config`
- `NEWS_API_KEY` - NewsAPI key
- `OPENAI_API_KEY` - OpenAI key
- `EMAIL_SENDER` - Gmail account
- `EMAIL_PASSWORD` - App password
- `EMAIL_RECIPIENT` - Where to send emails
- `NEWS_TOPIC` - Topic to search
- `MAX_ARTICLES` - Number of articles to fetch

**Validation:** `Config.validate()` checks all required keys are set

---

### fetch_news.py
**Purpose:** PHASE 1 - Fetch articles from NewsAPI

**Main function:** `fetch_news(topic=None, max_articles=None)`
- Takes topic and max article count
- Queries NewsAPI endpoint
- Cleans data (removes None values)
- Returns structured list

**Output format:**
```python
[
    {
        "title": "Article Title",
        "description": "Article summary...",
        "url": "https://...",
        "source": "News Source",
        "publishedAt": "2024-12-25T08:00:00Z"
    },
    ...
]
```

---

### summarize.py
**Purpose:** PHASE 2 - AI-powered news summarization

**Main function:** `summarize_news(articles)`
- Takes list of articles
- Creates OpenAI prompt
- Calls GPT-3.5-turbo API
- Returns 3 bullet points

**Prompt engineering:**
- System prompt: Financial news analyst persona
- User prompt: Articles + instructions
- Output format: 3 bullet points, under 60 seconds

**Example output:**
```
• Bullet point 1 about important development
• Bullet point 2 about market trend
• Bullet point 3 about key announcement
```

---

### emailer.py
**Purpose:** PHASE 3 - Email automation

**Main function:** `send_email(subject, summary, articles, recipient)`
- Creates email message
- Formats HTML template
- Connects to Gmail SMTP
- Authenticates
- Sends email

**Email includes:**
- Header with branding
- Summary bullet points
- Full article links
- Professional footer

---

### .env
**Purpose:** Store secrets (API keys, passwords)

**What goes here:**
- NewsAPI key
- OpenAI key
- Gmail credentials
- Email recipient
- News topic preference

**⚠️ SECURITY:**
- Never commit to Git
- Never share with others
- `.gitignore` protects it

---

## 🔄 Data Flow

```
┌─────────────────┐
│   NewsAPI       │
│   (questions:   │
│   "Indian       │
│    Startups")   │
└────────┬────────┘
         │ returns 10 articles
         ▼
┌─────────────────────────────────┐
│   fetch_news.py                 │
│   Cleans & formats articles     │
│   Returns: [title, desc, url]   │
└────────┬────────────────────────┘
         │ sends to GPT
         ▼
┌─────────────────────────────────┐
│   summarize.py                  │
│   Calls OpenAI API              │
│   Returns: 3 bullets            │
└────────┬────────────────────────┘
         │ combines with articles
         ▼
┌─────────────────────────────────┐
│   emailer.py                    │
│   Creates HTML email            │
│   Sends via Gmail SMTP          │
└─────────────────────────────────┘
         │
         ▼
    📧 Your Inbox
```

---

## 🎯 Project Phases

| Phase | File | What It Does |
|-------|------|------------|
| 0 | - | Planning & architecture |
| 1 | fetch_news.py | Fetch articles from API |
| 2 | summarize.py | Summarize with AI |
| 3 | emailer.py | Send email |
| 4 | main.py | Scheduling setup |
| 5 | config.py + .env | Secure credentials |
| 6 | README.md | Documentation |

---

## 🧪 Testing Checklist

- [ ] `python config.py` - Validate configuration
- [ ] `python fetch_news.py` - Test news fetching
- [ ] `python summarize.py` - Test summarization
- [ ] `python emailer.py` - Test email
- [ ] `python main.py --no-email` - Full pipeline without email
- [ ] `python main.py` - Full pipeline with email
- [ ] Check inbox for email
- [ ] Schedule with Task Scheduler/Cron

---

## 💡 Tips & Tricks

### Get Started Fastest
```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
# Edit .env with your API keys

# 3. Test
python main.py --no-email

# 4. Email
python main.py
```

### Test Specific Features
```bash
# Test news fetching only
python fetch_news.py

# Test summarization only
python summarize.py

# Test email sending only
python emailer.py

# Full pipeline without email
python main.py --no-email
```

### Customize for Your Needs
```bash
# Different topic
python main.py --topic "Tech News"

# More articles
python main.py --max-articles 20

# Different recipient
python main.py --recipient boss@company.com

# Combine
python main.py --topic "AI" --max-articles 15 --recipient team@company.com
```

---

## 🆘 Need Help?

### Check Documentation
1. **README.md** - Overview and features
2. **SETUP.md** - Detailed setup instructions
3. **SCHEDULING.md** - Automation guide
4. **Code comments** - Read the code itself!

### Common Issues
- **API keys not working?** Check .env file syntax
- **Email not sending?** Use Gmail App Password, not regular password
- **No articles found?** Check NewsAPI free tier limits
- **Rate limit?** Wait 1 minute before retrying

### Error Messages
Most error messages in the code are descriptive. They tell you exactly what's wrong!

---

## 📱 Share Your Success!

Once you get it working:
1. Push to GitHub
2. Add to your portfolio
3. Write a blog post
4. Share on LinkedIn/Twitter
5. Mention in interviews!

**Talking points:**
- "Built an automated news processing pipeline with Python"
- "Integrated NewsAPI and OpenAI APIs"
- "Implemented AI-powered content generation"
- "Set up daily automation with scheduling"
- "Used secure credential management with .env"

---

## 🗂️ File Organization

```
news-flash/
├── README.md              # Start here!
├── SETUP.md              # Setup guide
├── SCHEDULING.md         # How to automate
├── EXAMPLE_OUTPUT.md     # See examples
├── INDEX.md              # This file
│
├── main.py               # RUN THIS
├── config.py             # Configuration
├── fetch_news.py         # Phase 1
├── summarize.py          # Phase 2
├── emailer.py            # Phase 3
│
├── .env                  # Your secrets
├── requirements.txt      # Dependencies
└── .gitignore           # Git ignore
```

---

## ✨ You're All Set!

Everything you need is in this directory. Pick a starting point and go! 🚀

**Recommended path:**
1. Read [README.md](README.md)
2. Follow [SETUP.md](SETUP.md)
3. Run `python main.py`
4. Check your email!

Happy coding! 🎉
