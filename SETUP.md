# 🚀 News-Flash: Complete Setup Guide

This is the step-by-step guide to get News-Flash running in 15 minutes.

---

## ✅ Pre-Setup Checklist

- [ ] Python 3.8+ installed ([Download](https://www.python.org/downloads/))
- [ ] GitHub account (for portfolio)
- [ ] NewsAPI account (free tier at [newsapi.org](https://newsapi.org))
- [ ] OpenAI account with API credits ([Sign up](https://platform.openai.com))
- [ ] Gmail account for sending emails
- [ ] Text editor (VS Code, PyCharm, etc.)

---

## 📋 Step 1: Get Your API Keys (10 minutes)

### 1.1 NewsAPI Key
1. Go to [newsapi.org](https://newsapi.org)
2. Click "Register"
3. Sign up with email
4. Go to your account dashboard
5. Copy the **API Key** (free tier available)

**Free Tier Limits:**
- 100 requests per day
- Top 1 month old articles
- Perfect for learning!

### 1.2 OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or login
3. Go to API keys section
4. Create new secret key
5. Copy the key (store safely, don't share!)

**Pricing:**
- GPT-3.5-turbo: ~$0.002 per 1K tokens (very cheap!)
- Add payment method to use API
- You get $5 free credits when you start

### 1.3 Gmail App Password
1. Enable 2-Factor Authentication on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Select "Mail" and "Windows Computer" (or your device)
4. Google generates a 16-character password
5. Copy this password (not your Gmail password!)

**Why App Password?**
- More secure than regular password
- Can be revoked anytime
- Best practice for automation

---

## 🎯 Step 2: Clone & Setup Project (5 minutes)

### Option A: Clone from GitHub (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/news-flash.git
cd news-flash

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Manual Setup
```bash
# Create folder
mkdir news-flash
cd news-flash

# Copy all files from this directory

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install packages
pip install requests python-dotenv openai
```

---

## 🔐 Step 3: Configure Environment Variables (2 minutes)

1. Open `.env` file in the project directory
2. Fill in your credentials:

```env
# NewsAPI Configuration
NEWS_API_KEY=your_newsapi_key_here
# Example: abc123def456ghi789jkl012mno345pqr

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
# Example: sk-proj-abc123...

# Email Configuration
EMAIL_SENDER=your_email@gmail.com
# Example: john.doe@gmail.com

EMAIL_PASSWORD=your_app_password_here
# Example: abcd efgh ijkl mnop (16 chars, with space)

EMAIL_RECIPIENT=recipient@example.com
# Can be same as EMAIL_SENDER or different

# News Topic
NEWS_TOPIC=Indian Startups
# Change this to any topic you want!
```

**⚠️ IMPORTANT:**
- Never commit `.env` to GitHub
- Keep API keys secret
- `.gitignore` already protects it

---

## ✨ Step 4: Test Your Setup (2 minutes)

### Test 1: Validate Configuration
```bash
python config.py
```

**Expected Output:**
```
✓ Configuration validated successfully!
```

### Test 2: Fetch News
```bash
python fetch_news.py
```

**Expected Output:**
```
📡 Fetching news for: Indian Startups...
✓ Successfully fetched 10 articles
📰 Article 1: Title of article...
```

### Test 3: Test Summarization
```bash
python summarize.py
```

**Expected Output:**
```
📡 Fetching news for: Indian Startups...
✓ Successfully fetched 10 articles
🧠 Generating AI summary...
✓ Summary generated successfully

📊 Generated Summary:
• Bullet point 1...
• Bullet point 2...
• Bullet point 3...
```

### Test 4: Run Complete Pipeline (No Email)
```bash
python main.py --no-email
```

**Expected Output:**
```
============================================================
🚀 NEWS-FLASH: 60-Second News Summarizer
============================================================
[PHASE 1] Fetching News Articles...
✓ Phase 1 Complete: 10 articles fetched

[PHASE 2] Generating AI Summary...
✓ Phase 2 Complete: Summary generated

[PHASE 3] Skipped: Email notification disabled

============================================================
✅ PIPELINE COMPLETED SUCCESSFULLY!
============================================================
```

### Test 5: Send Test Email
```bash
python main.py
```

Check your email inbox! You should receive the formatted digest.

---

## 📅 Step 5: Schedule Daily Runs (2 minutes)

Choose your platform:

### Windows Users:
```powershell
# Open PowerShell as Administrator
# Run:
schtasks /create /tn "NewsFlash Daily" /tr "C:\path\to\python.exe C:\path\to\news-flash\main.py" /sc daily /st 08:00:00

# Verify:
schtasks /query /tn "NewsFlash Daily"
```

See [SCHEDULING.md](SCHEDULING.md) for detailed GUI instructions.

### macOS/Linux Users:
```bash
# Edit crontab
crontab -e

# Add this line:
0 8 * * * cd /path/to/news-flash && /usr/bin/python3 main.py

# Verify:
crontab -l
```

See [SCHEDULING.md](SCHEDULING.md) for more methods.

---

## 🧪 Advanced Testing

### Test with Different Topic
```bash
python main.py --topic "Tesla News"
```

### Test with Custom Recipient
```bash
python main.py --recipient test@example.com
```

### Fetch More Articles
```bash
python main.py --max-articles 20
```

### Combine Options
```bash
python main.py --topic "Cryptocurrency" --no-email --max-articles 15
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### "Invalid API key"
- ✓ Check you copied the key correctly
- ✓ Ensure key has no spaces
- ✓ Verify it's in the `.env` file

### "Email authentication failed"
- ✓ For Gmail: Use App Password, not your Gmail password
- ✓ Enable 2FA at [myaccount.google.com](https://myaccount.google.com)
- ✓ Generate App Password at [apppasswords](https://myaccount.google.com/apppasswords)

### "No articles found"
- ✓ NewsAPI free tier has 100 requests/day limit
- ✓ Try a more common topic
- ✓ Check usage at [newsapi.org/account](https://newsapi.org/account)

### "Rate limit exceeded"
- ✓ OpenAI: Wait 1 minute before retrying
- ✓ Upgrade plan if this keeps happening
- ✓ Check usage at [platform.openai.com/account/usage](https://platform.openai.com/account/usage)

---

## 💰 Cost Estimation

| Service | Free Limit | Cost |
|---------|-----------|------|
| **NewsAPI** | 100 requests/day | Free tier is enough! |
| **OpenAI** | $5 startup credits | ~$0.002 per summary (very cheap) |
| **Gmail** | Unlimited | Free |

**Monthly Cost:**
- Daily run (30 summaries): ~$0.06 ✨

---

## 📊 Project Structure Explained

```
news-flash/
├── main.py              # ⭐ Main entry point (run this!)
├── fetch_news.py        # Get articles from NewsAPI
├── summarize.py         # Use OpenAI to summarize
├── emailer.py           # Send emails via Gmail
├── config.py            # Load environment variables
├── .env                 # Your API keys (KEEP SECRET!)
├── requirements.txt     # Python dependencies
├── README.md            # Full documentation
├── SCHEDULING.md        # How to automate
├── SETUP.md             # This file
└── EXAMPLE_OUTPUT.md    # Example output
```

---

## 🎓 Learning Paths

### Path 1: Understanding the Code
1. Read `README.md` for overview
2. Review `config.py` - how environment variables work
3. Study `fetch_news.py` - API integration pattern
4. Examine `summarize.py` - prompt engineering
5. Check `emailer.py` - SMTP automation
6. Explore `main.py` - orchestration

### Path 2: Production Deployment
1. Set up Python virtual environment
2. Configure secure environment variables
3. Test all functionality
4. Schedule with Task Scheduler/Cron
5. Monitor logs
6. Scale to multiple topics

### Path 3: Portfolio Enhancement
1. Add this to your GitHub
2. Write a portfolio post: "Building an Autonomous AI News Pipeline"
3. Demonstrate:
   - API integration
   - Prompt engineering results
   - Error handling
   - Production scheduling
4. Mention it in interviews!

---

## 🚀 Next Steps

- [ ] Complete all tests above
- [ ] Schedule daily runs
- [ ] Check first email delivery
- [ ] Push to GitHub
- [ ] Write portfolio post
- [ ] Share on LinkedIn/Twitter
- [ ] Consider improvements (caching, multiple topics, web dashboard)

---

## 📞 Quick Reference

**Run the web application:**
```bash
C:/Users/HP/Desktop/news_crux/.venv/Scripts/python.exe webapp/app.py
# Then open http://localhost:5000 in your browser
```

**Run the CLI pipeline:**
```bash
python main.py
```

**Test CLI without email:**
```bash
python main.py --no-email
```

**View all options:**
```bash
python main.py --help
```

**Check configuration:**
```bash
python config.py
```

---

## ✅ Success Checklist

When you see this, you're done! ✨

```
============================================================
✅ PIPELINE COMPLETED SUCCESSFULLY!
⏰ Finished at: 2024-12-25 08:00:42
============================================================
```

And in your email inbox:
```
From: your_email@gmail.com
Subject: 🗞️ News-Flash | Indian Startups

📌 KEY HIGHLIGHTS

• Bullet point 1...
• Bullet point 2...
• Bullet point 3...

📚 Full Articles
- Article 1 link
- Article 2 link
```

---

## 🎉 Congratulations!

You now have a fully automated AI-powered news summarization system! 

**Resume talking points:**
- ✅ Built end-to-end data pipeline
- ✅ Integrated with multiple APIs
- ✅ Used LLMs for content generation
- ✅ Implemented automation and scheduling
- ✅ Managed secure credentials
- ✅ Created production-ready code

---

**Made with ❤️ - Now go build amazing things!** 🚀
