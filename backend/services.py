"""
=========================================================
CANIS AI Services
Conversational Assistant for Natural Intelligence & Support
=========================================================
"""

from groq import Groq
from sqlalchemy.orm import Session

from config import (
    GROQ_API_KEY,
    MODEL,
    APP_NAME,
    APP_VERSION
)
from prompts import SYSTEM_PROMPT

from database import (
    ChatHistory,
    UploadedFile,
    Feedback
)


# ==========================================
# Groq Client
# ==========================================

client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# Save Chat
# ==========================================

def save_chat(

    db: Session,

    role: str,

    message: str

):

    chat = ChatHistory(

        role=role,

        message=message

    )

    db.add(chat)

    db.commit()


# ==========================================
# Get Conversation History
# ==========================================

def get_history(

    db: Session,

    limit: int = 20

):

    history = (

        db.query(ChatHistory)

        .order_by(ChatHistory.id.desc())

        .limit(limit)

        .all()

    )

    history.reverse()

    return history


# ==========================================
# Clear History
# ==========================================

def clear_history(

    db: Session

):

    db.query(ChatHistory).delete()

    db.commit()


# ==========================================
# Build Messages
# ==========================================

def build_messages(

    db: Session,

    user_message: str

):

    messages = [

        {

            "role": "system",

            "content": SYSTEM_PROMPT

        }

    ]

    history = get_history(db)

    for item in history:

        messages.append(

            {

                "role": item.role,

                "content": item.message

            }

        )

    messages.append(

        {

            "role": "user",

            "content": user_message

        }

    )

    return messages


# ==========================================
# AI Chat
# ==========================================

import re

def chat_with_canis(

    db: Session,

    message: str

):

    save_chat(
        db,
        "user",
        message
    )

    messages = build_messages(
        db,
        message
    )

    response = client.chat.completions.create(

        model=MODEL,

        messages=messages,

        temperature=0.7,

        max_completion_tokens=1024

    )

    # Get AI response
    answer = response.choices[0].message.content

    # -------------------------------
    # Clean AI response
    # -------------------------------

    # Remove HTML tags like <big>, <h1>, etc.
    answer = re.sub(r"<[^>]+>", "", answer)

    # Remove Markdown headings
    answer = re.sub(r"^#+\s*", "", answer, flags=re.MULTILINE)

    # Remove unwanted emojis
    answer = re.sub(r"[🐾🐺🎉✨💖💕😊🤗😍🥳🎊🎈]", "", answer)

    # Remove excessive blank lines
    answer = re.sub(r"\n{3,}", "\n\n", answer)

    # Remove leading/trailing spaces
    answer = answer.strip()

    save_chat(
        db,
        "assistant",
        answer
    )

    return answer

# ==========================================
# Save Uploaded File
# ==========================================

def save_uploaded_file(

    db: Session,

    filename: str,

    filepath: str

):

    file = UploadedFile(

        filename=filename,

        filepath=filepath

    )

    db.add(file)

    db.commit()


# ==========================================
# Save Feedback
# ==========================================

def save_feedback(

    db: Session,

    rating: int,

    comment: str

):

    feedback = Feedback(

        rating=rating,

        comment=comment

    )

    db.add(feedback)

    db.commit()


# ==========================================
# Health
# ==========================================

def health():

    return {

        "status": "running",

        "app": APP_NAME,

        "version": APP_VERSION,

        "model": MODEL

    }