"""
=====================================================
CANIS AI Configuration
Conversational Assistant for Natural Intelligence & Support
=====================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# ===============================
# Base Directory
# ===============================

BASE_DIR = Path(__file__).resolve().parent


# ===============================
# Load Environment Variables
# ===============================

load_dotenv(BASE_DIR / ".env")


# ===============================
# Application Info
# ===============================

APP_NAME = "CANIS AI"

APP_VERSION = "1.0.0"

DESCRIPTION = (
    "Conversational Assistant for Natural Intelligence & Support"
)


# ===============================
# Server Settings
# ===============================

HOST = os.getenv(
    "HOST",
    "0.0.0.0"
)

PORT = int(
    os.getenv(
        "PORT",
        8000
    )
)

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() == "true"


# ===============================
# Groq AI Settings
# ===============================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


MODEL = os.getenv(
    "MODEL",
    "llama-3.3-70b-versatile"
)

# Upload Settings

UPLOAD_FOLDER = BASE_DIR / "uploads"

UPLOAD_FOLDER.mkdir(exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024


# Allowed File Types

ALLOWED_EXTENSIONS = {

    "txt",
    "pdf",
    "doc",
    "docx",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "csv",
    "xlsx",
    "ppt",
    "pptx",
    "zip",
    "py",
    "js",
    "html",
    "css",
    "json"

}
# ===============================
# Chat Settings
# ===============================

MAX_MESSAGE_LENGTH = 5000

MAX_HISTORY = 20


# ===============================
# Frontend Access
# ===============================

ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "http://localhost:8000",

    "https://heroic-bonbon-262a8a.netlify.app"
]


# ===============================
# Validation
# ===============================

if not GROQ_API_KEY:

    print(
        "⚠️ WARNING: GROQ_API_KEY missing"
    )


# ===============================
# Startup Information
# ===============================

print("===============================")

print("🐺 CANIS AI Configuration Loaded")

print("===============================")

print(
    f"Model : {MODEL}"
)

print(
    f"Debug : {DEBUG}"
)

print("===============================")