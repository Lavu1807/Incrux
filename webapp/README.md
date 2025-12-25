# 🌐 News-Flash Web Application

Multi-user web application for personalized AI-powered news summaries.

## Features

- User authentication with secure password hashing
- Personalized news topics per user
- AI-powered summarization (Google Gemini or OpenAI GPT)
- SQLite database for user and preference management
- Professional, clean responsive UI design
- Solid color scheme with modern typography
- Real-time news fetching and summarization

## Quick Start

### 1. Install Dependencies
```bash
C:/Users/HP/Desktop/news_crux/.venv/Scripts/python.exe -m pip install -r ../requirements.txt
```

### 2. Set Environment Variables
Edit the parent `.env` file with your API keys:
- NEWS_API_KEY
- AI_PROVIDER (OPENAI or GEMINI)
- GEMINI_API_KEY (if using Gemini)
- OPENAI_API_KEY (if using OpenAI)

### 3. Run the Web App
```bash
C:/Users/HP/Desktop/news_crux/.venv/Scripts/python.exe app.py
```

### 4. Open in Browser
Navigate to: http://localhost:5000

## Usage

1. **Sign Up**: Create a new account
2. **Login**: Access your dashboard
3. **Add Topics**: Add news topics you're interested in
4. **View News**: Click "View News" on any topic to see:
   - AI-generated 3-bullet summary
   - Full list of articles with links

## Database

The app uses SQLite with two tables:
- `User`: stores user accounts
- `NewsPreference`: stores user's news topics

Database file: `newsflash.db` (created automatically on first run)

## Security

- Passwords are hashed using Werkzeug's pbkdf2:sha256
- Flask-Login handles session management
- Set `FLASK_SECRET_KEY` environment variable in production

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3 (embedded, professional design)
- **Database**: SQLite
- **AI Provider**: Google Gemini or OpenAI GPT (configurable)
- **News Source**: NewsAPI
- **Design**: Solid colors, system fonts, responsive layout

## Development

To run in debug mode (auto-reload on changes):
```bash
C:/Users/HP/Desktop/news_crux/.venv/Scripts/python.exe app.py
```
(Debug mode is enabled by default in app.py)

## Production Deployment

For production:
1. Set `app.run(debug=False)`
2. Set strong `FLASK_SECRET_KEY` in environment
3. Use a production WSGI server (gunicorn, waitress)
4. Consider PostgreSQL instead of SQLite
5. Add rate limiting and CSRF protection

## API Rate Limits

- NewsAPI: 100 requests/day (free tier)
- Gemini: Check your quota at Google AI Studio
- OpenAI: Based on your billing plan

## Troubleshooting

**Database locked error**: Close all connections, restart the app

**Import errors**: Ensure you're in the webapp directory or parent path is correct

**API errors**: Check `.env` file has correct keys with no extra spaces
