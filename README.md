# 🗞️ Incrux | News-Flash

**Automated daily news digests with AI. Fetch, summarize, and deliver in under 60 seconds.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

## 🎯 Overview

Incrux bundles a CLI pipeline and a Flask web app to turn raw news into concise, actionable digests. It can run headless on a schedule or serve multiple users with per-topic dashboards backed by SQLite.

Pipeline steps:
1. Fetch the latest articles for a topic from NewsAPI
2. Summarize to exactly 3 crisp bullets via OpenAI GPT or Google Gemini (with local fallback)
3. Email an HTML digest with links (optional)

## ✨ Key Features

- Real-time NewsAPI fetching with topic + max-article control
- Dual AI providers (OpenAI or Gemini) with graceful local fallback
- Multi-user Flask web UI with sign-up/login and per-user topics
- HTML email digests plus plaintext, SMTP via Gmail
- CLI pipeline with switches for topic, recipient, max articles, and email toggle
- Scheduling-friendly (Task Scheduler/Cron); all secrets pulled from `.env`

## 🛠️ Tech Stack

| Component | Technology |
| --- | --- |
| News source | NewsAPI |
| AI engine | OpenAI Chat Completions or Google Gemini |
| Web | Flask, Flask-Login, SQLAlchemy |
| Database | SQLite |
| Email | Gmail SMTP (TLS) |
| Language | Python 3.10+ |

## 📋 Project Structure

```
incrux/
├── main.py             # CLI entry: fetch → summarize → email
├── fetch_news.py       # NewsAPI integration
├── summarize.py        # AI summarization + fallback
├── emailer.py          # HTML/plaintext email sending
├── config.py           # Env-driven configuration and validation
├── requirements.txt
├── webapp/
│   ├── app.py          # Flask app (auth, topics, dashboards)
│   ├── migrate_db.py   # DB migration helper
│   ├── send_scheduled_emails.py
│   └── templates/      # UI templates (dashboard, login, news, etc.)
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ and git
- API keys: NewsAPI, plus OpenAI or Gemini
- Gmail account with an App Password for SMTP

### 1) Clone and install
```bash
git clone https://github.com/Lavu1807/Incrux.git
cd Incrux
python -m venv .venv
.venv\Scripts\activate        # PowerShell
pip install -r requirements.txt
```

### 2) Configure `.env`
Create `.env` in the repo root:
```bash
# NewsAPI
NEWS_API_KEY=your_newsapi_key

# AI provider (OPENAI or GEMINI)
AI_PROVIDER=OPENAI
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo
# GEMINI_API_KEY=your_gemini_key
# GEMINI_MODEL=gemini-1.5-flash

# Email
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient@example.com

# Defaults
NEWS_TOPIC=Indian Startups
MAX_ARTICLES=10

# Flask (web app)
FLASK_SECRET_KEY=change-me-in-production
```

### 3) Run the CLI pipeline
```bash
python main.py                       # default topic + email
python main.py --topic "AI"          # custom topic
python main.py --max-articles 20
python main.py --no-email            # skip SMTP (test mode)
python main.py --recipient you@org.com
```

### 4) Run the web app
```bash
python webapp/app.py
# open http://localhost:5000
# sign up, add topics, and view summaries
```

The first run creates `newsflash.db` automatically. Each user can manage their own topics and article limits.

## 📅 Scheduling

- **Windows Task Scheduler:** point to `python main.py` inside the repo directory.
- **Cron (Linux/Mac):** `0 8 * * * cd /path/to/Incrux && /usr/bin/python3 main.py`.

## 🔒 Security Notes

- Keep `.env` out of version control (already in `.gitignore`).
- Use Gmail App Passwords (not your regular password) when SMTP auth is enabled.
- Set a strong `FLASK_SECRET_KEY` in production and switch Flask `debug` off for deployment.

## 🧠 Email Output Preview

Subject: `🗞️ News-Flash | Indian Startups`

```
📌 KEY HIGHLIGHTS:
• Indian fintech startups raised $120M this week...
• Government announced new incentives for early-stage SaaS companies...
• Tech layoffs declined by 18% YoY...

📚 FULL ARTICLES:
- "India's Startup Funding Hits $15B in 2023..." - TechCrunch
- "GST incentives for SaaS startups..." - LiveMint
- "Tech Job Market Stabilizes..." - YourStory
```

## 🧭 Troubleshooting

- `Configuration Error`: ensure required keys exist in `.env`; AI provider key must match `AI_PROVIDER`.
- `SMTPAuthenticationError`: verify Gmail App Password and 2FA; keep TLS port 587.
- `No articles found`: adjust topic wording or increase `MAX_ARTICLES`.
- `Import errors` in web app: run from project root so `webapp/app.py` can import shared modules.
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

**Made by Lavanya Verma**

*P.S. - This project went from zero to production in one afternoon. Imagine what we can build together.* 🚀
