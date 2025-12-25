# Email Scheduling Guide

## Overview

News-Flash now supports **personalized email scheduling**. Each user can choose:
- **Preferred Time**: When they want to receive daily news summaries
- **Email Toggle**: Enable/disable email notifications

## User Features

### Setting Email Preferences

**1. During Signup:**
- Choose your preferred email time (default: 08:00 AM)
- Enable/disable email summaries
- Time is in 24-hour format (e.g., 14:30 = 2:30 PM)

**2. In Profile Settings:**
- Navigate to Profile page
- Update "Email Preferences" section
- Change preferred time or toggle email on/off
- Click "Save Preferences"

## Email Scheduling System

### How It Works

1. **Database Storage**: User's `preferred_email_time` and `email_enabled` status stored in database
2. **Scheduled Script**: `send_scheduled_emails.py` runs every hour
3. **Time Matching**: Script checks if current hour matches any user's preferred time
4. **Email Sending**: Sends personalized news summaries for all user topics

### Database Schema

**User Table Fields:**
```python
preferred_email_time = db.Column(db.String(5), default='08:00')  # Format: HH:MM
email_enabled = db.Column(db.Boolean, default=True)
```

## Setting Up Automation

### Windows Task Scheduler

**Create Hourly Task:**

1. Open Task Scheduler
2. Create Basic Task → Name: "News-Flash Email Sender"
3. Trigger: Daily, starting at 00:00
4. Action: Start a Program
   - Program: `C:/Users/HP/Desktop/news_crux/.venv/Scripts/python.exe`
   - Arguments: `c:\Users\HP\Desktop\news_crux\news-flash\webapp\send_scheduled_emails.py`
   - Start in: `c:\Users\HP\Desktop\news_crux\news-flash\webapp`
5. Advanced Settings:
   - Check "Repeat task every: 1 hour"
   - Check "For a duration of: Indefinitely"
   - Check "Run task as soon as possible after a scheduled start is missed"

### Linux/Mac (Cron)

**Edit crontab:**
```bash
crontab -e
```

**Add hourly job:**
```bash
# Run every hour at minute 0
0 * * * * /path/to/venv/bin/python /path/to/webapp/send_scheduled_emails.py >> /path/to/logs/email_sender.log 2>&1
```

### Manual Testing

**Test the scheduler:**
```bash
# Activate virtual environment
C:/Users/HP/Desktop/news_crux/.venv/Scripts/activate

# Run the scheduler script
python webapp/send_scheduled_emails.py
```

**Expected Output:**
```
[2025-12-25 08:00:00] Checking for emails to send at 08:00
Found 3 users to send emails to

--- Processing user: john_doe (john@example.com) ---
  Fetching news for topic: Technology
  Found 10 articles for Technology
  Sending email to john@example.com
  ✓ Email sent successfully to john_doe

[2025-12-25 08:00:15] Email sending complete
```

## Example Usage

### User Workflow

**New User Signup:**
```
1. Sign up at http://localhost:5000/signup
2. Enter username, email, password
3. Set preferred email time: 07:00 (7 AM)
4. Check "Enable daily email summaries"
5. Submit form
6. Add topics in dashboard
7. Receive daily email at 7 AM with all topics
```

**Update Email Time:**
```
1. Login → Profile
2. Change preferred time to 18:00 (6 PM)
3. Save preferences
4. Next email arrives at 6 PM
```

**Disable Emails:**
```
1. Login → Profile
2. Uncheck "Enable daily email summaries"
3. Save preferences
4. No more automatic emails (can still view news in web app)
```

## Email Content

**Subject Line:**
```
News-Flash Daily Summary | Technology, AI, Business...
```

**Email Body:**
- Summary for each topic (with AI highlights)
- List of all articles with clickable links
- Professional HTML formatting
- Powered by NewsAPI and Gemini/OpenAI

## Configuration

### Environment Variables Required

```env
# Email Settings (for sending)
SENDER_EMAIL=your-email@gmail.com
SENDER_APP_PASSWORD=your-gmail-app-password

# Gmail SMTP (default)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# For Gmail: Enable 2FA and create App Password
# https://myaccount.google.com/apppasswords
```

### Email Settings for Gmail

1. Enable 2-Factor Authentication
2. Go to https://myaccount.google.com/apppasswords
3. Generate App Password for "Mail"
4. Use this password in `SENDER_APP_PASSWORD`

## Troubleshooting

### No Emails Received

**Check:**
1. Email is enabled in profile: `email_enabled = True`
2. Scheduler script is running hourly
3. Email credentials are correct in `.env`
4. User has topics added (no topics = no email)
5. Check script logs for errors

**Test Manually:**
```bash
# Run scheduler script to check for errors
python webapp/send_scheduled_emails.py
```

### Wrong Time Zone

The system uses server's local time. If emails arrive at wrong time:

**Solution 1: Adjust User Preference**
- If server is UTC and user is EST (-5 hours)
- User wants 8 AM EST = 1 PM UTC
- Set preferred time to 13:00

**Solution 2: Add Timezone Support**
- Install `pytz` package
- Add `timezone` field to User model
- Convert times in `send_scheduled_emails.py`

### Email Not Sending

**Common Issues:**
1. **Gmail App Password**: Must use App Password, not regular password
2. **SMTP Blocked**: Check firewall/antivirus
3. **Daily Limit**: Gmail has sending limits (500/day for free accounts)
4. **Invalid Email**: Check recipient email address

## Advanced Configuration

### Customize Email Frequency

**Current:** Daily (hourly check)

**To Add Weekly/Custom:**
```python
# Add to User model
email_frequency = db.Column(db.String(20), default='daily')  # daily, weekly, custom

# Modify send_scheduled_emails.py
if user.email_frequency == 'daily':
    # Send daily
elif user.email_frequency == 'weekly':
    # Check if today is user's preferred day
```

### Multiple Daily Emails

**Allow users to set multiple times:**
```python
# Change to JSON array
preferred_email_times = db.Column(db.JSON, default=['08:00'])

# In scheduler, loop through times
for time in user.preferred_email_times:
    if current_time.startswith(time.split(':')[0]):
        send_email(...)
```

### Custom Topics Per Time

**Advanced feature:**
- Morning: Business, Technology
- Evening: Sports, Entertainment
- Add `topic_schedules` JSON field to store mappings

## Architecture

```
User Signs Up
    ↓
Sets Preferred Email Time
    ↓
Adds Topics in Dashboard
    ↓
Task Scheduler runs send_scheduled_emails.py every hour
    ↓
Script checks current time vs user preferences
    ↓
Fetches news for all user topics
    ↓
Generates AI summaries
    ↓
Sends HTML email to user
    ↓
User receives personalized news summary
```

## Security Considerations

1. **Email Privacy**: User emails stored in database - use HTTPS in production
2. **App Passwords**: Store in `.env`, never commit to Git
3. **Rate Limiting**: Consider implementing rate limits to prevent abuse
4. **Unsubscribe**: Add unsubscribe link to emails (toggle `email_enabled`)

## Future Enhancements

- **Timezone Support**: Store user timezone for accurate delivery
- **Email Preview**: Show sample email before scheduling
- **Delivery Reports**: Track sent emails and open rates
- **Custom Templates**: Let users customize email format
- **Digest Options**: Daily/Weekly/Monthly frequency
- **Topic-Specific Times**: Different topics at different times

---

**Status:** Email scheduling feature fully implemented and documented ✅
