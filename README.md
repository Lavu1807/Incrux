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
# Windows (PowerShell)
$env:PORT=5050
python webapp/app.py

# macOS/Linux
PORT=5050 python webapp/app.py

# Then open http://localhost:5050 in your browser
# Sign up, log in, add topics, and view personalized news summaries
```

The first run creates `newsflash.db` automatically. Each user can manage their own topics and article limits.

**Note:** The app defaults to port 5000, but you can override it with the `PORT` environment variable if port 5000 is already in use.

## 📅 Scheduling

### CLI Pipeline (main.py)
- **Windows Task Scheduler:** point to `python main.py` inside the repo directory.
- **Cron (Linux/Mac):** `0 8 * * * cd /path/to/Incrux && /usr/bin/python3 main.py`.

### Scheduled Web App Emails (send_scheduled_emails.py)
For automated email delivery to web app users at their preferred times:

**Windows Task Scheduler (run as Administrator):**
```powershell
$python = "C:\Users\HP\Desktop\news_crux\.venv\Scripts\python.exe"
$script = "C:\Users\HP\Desktop\news_crux\incrux\webapp\send_scheduled_emails.py"
$action = New-ScheduledTaskAction -Execute $python -Argument $script
$trigger = New-ScheduledTaskTrigger -Hourly
Register-ScheduledTask -TaskName "NewsFlash-SendEmails" -Action $action -Trigger $trigger -RunLevel Highest
```

**Cron (Linux/Mac):**
```bash
# Run every hour
0 * * * * cd /path/to/Incrux/webapp && /usr/bin/python3 send_scheduled_emails.py
```

Make sure to set valid Gmail credentials in `.env` for email delivery to work.

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

### Issue: "Configuration Error" or Missing API keys

**Solution:**
- Ensure all required keys exist in `.env`
- AI provider key must match `AI_PROVIDER` setting (OPENAI or GEMINI)
- For NewsAPI: Get key at [newsapi.org](https://newsapi.org)
- For OpenAI: Get key at [platform.openai.com](https://platform.openai.com)
- For Gemini: Get key at [aistudio.google.com](https://aistudio.google.com)

### Issue: "Invalid API key" error

**Solution:**
- Verify you copied the key correctly (no extra spaces)
- Check that the key has not been revoked in the provider's dashboard
- For OpenAI/Gemini: Ensure you have an active payment method

### Issue: Web app says "site cannot be reached" on port 5000

**Solution:**
- Another service may be using port 5000
- Run the app on an alternate port:
  ```powershell
  $env:PORT=5050
  python webapp/app.py
  ```
- Then open http://127.0.0.1:5050

### Issue: Email not sending from web app

**Solution:**
- Update `.env` with real Gmail credentials (currently has placeholders):
  ```env
  EMAIL_SENDER=your_actual_email@gmail.com
  EMAIL_PASSWORD=your_16_char_app_password
  EMAIL_RECIPIENT=your_email@gmail.com
  ```
- Ensure `send_scheduled_emails.py` is scheduled in Task Scheduler/Cron
- Test the script manually:
  ```powershell
  cd "C:\Users\HP\Desktop\news_crux\incrux\webapp"
  python send_scheduled_emails.py
  ```
- Check that user has email enabled and preferred time is set in profile

### Issue: Gemini model errors

**Solution:**
- The system automatically tries multiple Gemini models (latest first) and falls back to local summary if all fail
- If you see "404 models/... not found": this is normal, the script will retry with alternate models
- Consider using OpenAI instead by setting `AI_PROVIDER=OPENAI` in `.env`

### Issue: No articles found

**Solution:**
- NewsAPI free tier has 100 requests/day limit. Check usage at [newsapi.org/account](https://newsapi.org/account)
- Try a more common topic (e.g., "Technology", "Business")
- Increase `--max-articles` parameter
- Verify NewsAPI key is valid

### Issue: Rate limit exceeded

**Solution:**
- OpenAI: Upgrade plan or reduce request frequency
- NewsAPI: Wait 24 hours or upgrade plan
- Gemini: Public API has quotas; check [Google Cloud Console](https://console.cloud.google.com)

---

## 🔄 Recent Updates (Dec 2025)

- **Improved Gemini fallback:** Automatically tries multiple Gemini model versions if the primary fails
- **Configurable web app port:** Use `PORT` environment variable to avoid conflicts
- **Fixed scheduled email script:** Now correctly finds database and initializes tables
- **Better error handling:** Graceful fallback to local summaries when APIs are unavailable or rate-limited

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
