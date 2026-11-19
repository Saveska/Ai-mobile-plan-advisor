import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Centralized configuration class.
    All environment variables and constants are defined here
    to keep the application maintainable and secure.
    """

    # AI
    GROQ_API_KEY = os.getenv("API_KEY")

    # Email
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
