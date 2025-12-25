# Email Scheduling - Quick Setup Guide

## What's New? 🎉

Users can now **choose when they want to receive daily news summaries**!

### New Features:
- ⏰ **Custom Email Time** - Pick any time (e.g., 7:00 AM, 6:00 PM)
- ✉️ **Email Toggle** - Enable/disable email notifications
- 📧 **Personalized Delivery** - Each user gets their own schedule

---

## For Users

### 1. Set Email Preferences During Signup

When creating an account at [http://localhost:5000/signup](http://localhost:5000/signup):

1. Fill in username, email, password
2. **Choose "Preferred Email Time"** (default: 08:00)
3. Check/uncheck **"Enable daily email summaries"**
4. Click Sign Up

### 2. Update Email Settings Anytime

Go to **Profile** page ([http://localhost:5000/profile](http://localhost:5000/profile)):

1. See "Email Preferences" section
2. Change preferred time using time picker
3. Toggle email on/off
4. Click "Save Preferences"

### 3. How It Works

- **Set time to 07:00** → Receive email at 7 AM daily
- **Set time to 18:30** → Receive email at 6:30 PM daily
- **Disable emails** → Still access news on website, no emails
- **Enable emails** → Resume daily summaries at your preferred time

---

## For Administrators

### Setup Automated Email Sending

The email scheduler needs to run hourly to check for users ready to receive emails.

#### Windows Task Scheduler Setup

**1. Create the Task:**

```
Task Name: News-Flash Email Sender
Description: Sends scheduled news emails to users
```

**2. Trigger:**
- Begin: On a schedule
- Settings: Daily
- Start: 12:00:00 AM
- Recur every: 1 days
- Advanced: Repeat task every **1 hour** for a duration of **1 day**

**3. Action:**
- Action: Start a program
- Program/script: `C:\Users\HP\Desktop\news_crux\.venv\Scripts\python.exe`
- Add arguments: `c:\Users\HP\Desktop\news_crux\news-flash\webapp\send_scheduled_emails.py`
- Start in: `c:\Users\HP\Desktop\news_crux\news-flash\webapp`

**4. Conditions:**
- ✓ Start the task only if the computer is on AC power (optional)
- ✓ Wake the computer to run this task (optional)

**5. Settings:**
- ✓ Run task as soon as possible after a scheduled start is missed
- ✓ If the running task does not end when requested, force it to stop

#### Linux/Mac Cron Setup

```bash
# Edit crontab
crontab -e

# Add hourly job (runs at minute 0 of every hour)
0 * * * * /path/to/venv/bin/python /path/to/webapp/send_scheduled_emails.py >> /var/log/newsflash_emails.log 2>&1
```

### Test the Scheduler Manually

```powershell
# Activate virtual environment
C:/Users/HP/Desktop/news_crux/.venv/Scripts/activate

# Run scheduler script
python webapp/send_scheduled_emails.py
```

**Expected Output:**
```
[2025-12-25 08:00:00] Checking for emails to send at 08:00
Found 2 users to send emails to

--- Processing user: alice (alice@example.com) ---
  Fetching news for topic: Technology
  Found 10 articles for Technology
  Sending email to alice@example.com
  ✓ Email sent successfully to alice

--- Processing user: bob (bob@example.com) ---
  Fetching news for topic: Sports
  Found 8 articles for Sports
  Sending email to bob@example.com
  ✓ Email sent successfully to bob

[2025-12-25 08:00:15] Email sending complete
```

---

## Database Changes

### New Fields Added to User Table:

```python
preferred_email_time = db.Column(db.String(5), default='08:00')  # Format: HH:MM
email_enabled = db.Column(db.Boolean, default=True)
```

### Migration Required?

**If you have existing users:** 
- Stop the Flask app
- Delete `newsflash.db` (backs up user data first if needed)
- Restart app - new database will be created with updated schema

**If starting fresh:**
- No action needed - new database includes email fields automatically

---

## Email Requirements

### Environment Variables (.env)

```env
# Email sending credentials
SENDER_EMAIL=your-email@gmail.com
SENDER_APP_PASSWORD=your-app-password

# SMTP settings (Gmail default)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Gmail Setup

1. Enable 2-Factor Authentication on Gmail
2. Go to https://myaccount.google.com/apppasswords
3. Create App Password for "Mail"
4. Use this password in `SENDER_APP_PASSWORD`

---

## File Changes Summary

### Modified Files:
- ✅ `webapp/app.py` - Added email scheduling fields and profile update route
- ✅ `webapp/templates/signup.html` - Added email preference inputs
- ✅ `webapp/templates/profile.html` - Added email settings form

### New Files:
- ✅ `webapp/send_scheduled_emails.py` - Hourly email sender script
- ✅ `webapp/migrate_db.py` - Database migration helper
- ✅ `EMAIL_SCHEDULING.md` - Complete documentation
- ✅ `EMAIL_SCHEDULING_SETUP.md` - This quick guide

---

## Example User Flow

**Alice's Story:**

1. **Signs up at 9 AM**
   - Sets email time: 07:00
   - Enables email notifications

2. **Adds topics**
   - Technology
   - AI
   - Startups

3. **Next day at 7 AM**
   - Scheduler runs (checks all users)
   - Finds Alice's time matches
   - Fetches news for her 3 topics
   - Generates AI summaries
   - Sends combined email

4. **Alice reads email**
   - Subject: "News-Flash Daily Summary | Technology, AI, Startups"
   - 3 summarized sections with article links
   - Clicks links to read full articles

5. **Changes preference**
   - Goes to Profile → Email Preferences
   - Changes time to 18:00 (6 PM)
   - Now receives email in evening

---

## Troubleshooting

### Problem: No emails arriving

**Check:**
1. ✓ Email enabled in profile (`email_enabled = True`)
2. ✓ User has topics added (Dashboard → Add Topic)
3. ✓ Scheduler is running hourly (Task Scheduler/Cron)
4. ✓ Email credentials correct in `.env`
5. ✓ Gmail App Password configured

**Test:**
```bash
python webapp/send_scheduled_emails.py
```

### Problem: Email arrives at wrong time

**Cause:** Server timezone vs user timezone

**Solution:**
- Server time is what matters
- If server is UTC and you want 8 AM EST (-5 hours)
- Set preferred time to 13:00 (1 PM UTC = 8 AM EST)

### Problem: Multiple emails per hour

**Cause:** Scheduler running more frequently than hourly

**Solution:**
- Check Task Scheduler settings
- Ensure "Repeat task every: 1 hour"
- Not "1 minute" or "10 minutes"

---

## Production Deployment

### Considerations:

1. **Use Production SMTP**: Consider SendGrid, Mailgun for bulk emails
2. **Timezone Handling**: Add timezone field to User model
3. **Rate Limiting**: Respect email provider limits
4. **Unsubscribe Link**: Add to email footer
5. **Logging**: Store sent email records
6. **Error Handling**: Alert admins if sending fails

---

## Status

✅ **Feature Complete**
- User can set preferred email time
- User can enable/disable emails
- Scheduler sends personalized emails
- Profile page allows updates
- Documentation complete

**Next Steps:**
1. Configure Task Scheduler (Windows) or Cron (Linux)
2. Test with your Gmail credentials
3. Enjoy personalized news summaries!

---

**Need Help?** See [EMAIL_SCHEDULING.md](EMAIL_SCHEDULING.md) for detailed documentation.
