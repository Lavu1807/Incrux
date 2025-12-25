# 📅 News-Flash Scheduling Guide

This guide shows how to automate News-Flash to run daily at 8:00 AM on different platforms.

---

## Windows Task Scheduler (GUI Method)

### Step 1: Open Task Scheduler
- Press `Win + R`
- Type: `taskschd.msc`
- Press Enter

### Step 2: Create Basic Task
1. In the right panel, click **"Create Basic Task..."**
2. Name: `NewsFlash Daily`
3. Description: `Automated news summarization and email`
4. Click **Next**

### Step 3: Set Trigger
1. Select **Daily**
2. Click **Next**
3. Set start time: **8:00:00 AM**
4. Set start date: Today
5. Recurrence: Every 1 day
6. Click **Next**

### Step 4: Set Action
1. Select **Start a program**
2. Click **Next**
3. **Program/script**: `C:\Program Files\Python311\python.exe`
   - (Adjust path based on your Python installation)
4. **Add arguments**: `main.py`
5. **Start in**: `C:\path\to\news-flash`
   - Replace with your actual path
6. Click **Next**

### Step 5: Review & Finish
1. Review the summary
2. ☑ Check "Open the Properties dialog when I click Finish"
3. Click **Finish**

### Step 6: Configure Advanced Options (Important!)
In the Properties dialog:
1. **General Tab:**
   - ☑ Run whether user is logged in or not
   - ☑ Run with highest privileges

2. **Triggers Tab:**
   - Edit the trigger
   - ☑ Enabled

3. **Conditions Tab:**
   - ☐ Uncheck "Start the task only if the computer is on AC power"

4. **Settings Tab:**
   - ☑ Stop the task if it runs longer than: 1 hour
   - ☑ If the task fails, restart every: 1 hour

5. Click **OK**

### Testing the Task
```powershell
# Run manually to test
schtasks /run /tn "NewsFlash Daily"

# View all scheduled tasks
schtasks /query /tn "NewsFlash Daily" /v

# Delete task (if needed)
schtasks /delete /tn "NewsFlash Daily" /f
```

---

## Windows Command Line (PowerShell Script)

Create `schedule_news_flash.ps1`:

```powershell
# Define paths
$pythonPath = "C:\Program Files\Python311\python.exe"
$newsFlashPath = "C:\path\to\news-flash\main.py"
$workingDir = "C:\path\to\news-flash"

# Create the task
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $newsFlashPath -WorkingDirectory $workingDir
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
$principal = New-ScheduledTaskPrincipal -UserID "$env:USERNAME" -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable

$task = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -Settings $settings
Register-ScheduledTask -TaskName "NewsFlash Daily" -InputObject $task -Force

Write-Host "✓ Task 'NewsFlash Daily' created successfully!"
```

Run it:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\schedule_news_flash.ps1
```

---

## Linux Cron Job

### Method 1: Using crontab

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 8:00 AM)
0 8 * * * cd /home/username/news-flash && /usr/bin/python3 main.py >> /var/log/news-flash.log 2>&1
```

### Method 2: Systemd Timer (Modern Alternative)

Create `/etc/systemd/system/news-flash.service`:
```ini
[Unit]
Description=News-Flash Daily News Summarizer
After=network.target

[Service]
Type=oneshot
User=username
WorkingDirectory=/home/username/news-flash
Environment="PATH=/home/username/.local/bin:/usr/bin"
ExecStart=/usr/bin/python3 main.py
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/news-flash.timer`:
```ini
[Unit]
Description=Run News-Flash Daily
Requires=news-flash.service

[Timer]
OnCalendar=daily
OnCalendar=08:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable news-flash.timer
sudo systemctl start news-flash.timer

# Check status
sudo systemctl status news-flash.timer
```

View logs:
```bash
journalctl -u news-flash.service -f
```

---

## macOS LaunchAgent

Create `~/Library/LaunchAgents/com.newsflash.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.newsflash.daily</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/username/news-flash/main.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/username/news-flash</string>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/username/.newsflash/stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/username/.newsflash/stderr.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.newsflash.plist
launchctl start com.newsflash.daily

# Check status
launchctl list | grep newsflash

# Unload (if needed)
launchctl unload ~/Library/LaunchAgents/com.newsflash.plist
```

---

## GitHub Actions (Cloud-Based)

Create `.github/workflows/news-flash.yml`:

```yaml
name: News-Flash Daily

on:
  schedule:
    - cron: '0 8 * * *'  # 8:00 AM UTC every day
  workflow_dispatch:     # Allow manual trigger

jobs:
  news-flash:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run News-Flash
        env:
          NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          EMAIL_SENDER: ${{ secrets.EMAIL_SENDER }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_RECIPIENT: ${{ secrets.EMAIL_RECIPIENT }}
          NEWS_TOPIC: "Indian Startups"
        run: python main.py
      
      - name: Notify on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'News-Flash daily run failed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

Setup:
1. Push to GitHub
2. Go to Settings → Secrets and variables → Actions
3. Add repository secrets:
   - `NEWS_API_KEY`
   - `OPENAI_API_KEY`
   - `EMAIL_SENDER`
   - `EMAIL_PASSWORD`
   - `EMAIL_RECIPIENT`

---

## Verification & Monitoring

### Check if task is running

**Windows:**
```powershell
# View task history
Get-ScheduledTask -TaskName "NewsFlash Daily" | Get-ScheduledTaskInfo

# View last run time
Get-ScheduledTaskInfo -TaskName "NewsFlash Daily"
```

**Linux:**
```bash
# View cron logs
grep CRON /var/log/syslog

# Check last execution
last -f /var/log/wtmp
```

### Enable Logging

Add to your `.env`:
```env
LOG_LEVEL=INFO
LOG_FILE=/path/to/logs/news-flash.log
```

Then modify `main.py` to log:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news-flash.log'),
        logging.StreamHandler()
    ]
)
```

---

## Troubleshooting

### Task runs but produces no output
- Check that the working directory is correct
- Verify all environment variables are set in `.env`
- Check email credentials

### Task fails silently
- Test manually: `python main.py`
- Check Task Scheduler history for error codes
- Enable logging (see above)

### Email not sending at scheduled time
- Gmail may require app password instead of regular password
- Check that EMAIL_SENDER matches Gmail account
- Verify SMTP credentials in `.env`

### Permission denied errors
- Run task with highest privileges
- For Linux: Use sudo or proper user permissions

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| **Windows:** Run now | `schtasks /run /tn "NewsFlash Daily"` |
| **Windows:** View tasks | `schtasks /query` |
| **Linux:** View crontab | `crontab -l` |
| **Linux:** Edit crontab | `crontab -e` |
| **macOS:** Load agent | `launchctl load ~/Library/LaunchAgents/com.newsflash.plist` |
| **Test script** | `python main.py --no-email` |

---

**Need help?** Check the README.md for more information!
