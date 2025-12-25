"""
Configuration module for News-Flash.
Loads environment variables from .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to manage API keys and credentials."""
    
    # NewsAPI configuration
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    
    # Provider selection: OPENAI or GEMINI
    AI_PROVIDER = os.getenv("AI_PROVIDER", "OPENAI").upper()

    # OpenAI configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Gemini configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Email configuration
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # News topic
    NEWS_TOPIC = os.getenv("NEWS_TOPIC", "Indian Startups")
    
    # Number of articles to fetch
    MAX_ARTICLES = 10
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present."""
        required_keys = [
            "NEWS_API_KEY",
            "EMAIL_SENDER",
            "EMAIL_PASSWORD",
            "EMAIL_RECIPIENT"
        ]

        provider = cls.AI_PROVIDER
        if provider == "OPENAI":
            required_keys.append("OPENAI_API_KEY")
        elif provider == "GEMINI":
            required_keys.append("GEMINI_API_KEY")
        
        missing_keys = [key for key in required_keys if not getattr(cls, key, None)]
        
        if missing_keys:
            raise ValueError(f"Missing configuration keys: {', '.join(missing_keys)}. Please update .env file.")
        
        return True


if __name__ == "__main__":
    try:
        Config.validate()
        print("✓ Configuration validated successfully!")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
