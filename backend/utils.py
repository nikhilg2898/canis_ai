"""
=========================================================
CANIS AI Utilities
Conversational Assistant for Natural Intelligence & Support
=========================================================
"""

import os
import uuid
import html
from pathlib import Path
from datetime import datetime

from config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE
)


# =====================================================
# Escape HTML
# =====================================================

def escape_html(text: str) -> str:
    """
    Prevent HTML injection.
    """

    return html.escape(text)


# =====================================================
# Generate UUID
# =====================================================

def generate_id() -> str:
    """
    Generate unique ID.
    """

    return str(uuid.uuid4())


# =====================================================
# Timestamp
# =====================================================

def current_timestamp() -> str:
    """
    Current timestamp.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =====================================================
# Validate Extension
# =====================================================

def allowed_file(filename: str) -> bool:
    """
    Check file extension.
    """

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# =====================================================
# Validate File Size
# =====================================================

def validate_file_size(size: int):

    if size > MAX_FILE_SIZE:
        raise ValueError("File exceeds maximum allowed size.")


# =====================================================
# Format File Size
# =====================================================

def readable_size(size: int) -> str:

    units = [

        "B",
        "KB",
        "MB",
        "GB",
        "TB"

    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


# =====================================================
# Save Upload
# =====================================================

def save_upload(file, upload_dir: Path):

    upload_dir.mkdir(

        exist_ok=True

    )

    extension = Path(file.filename).suffix

    filename = f"{generate_id()}{extension}"

    filepath = upload_dir / filename

    with open(filepath, "wb") as buffer:

        buffer.write(file.file.read())

    return filename, filepath


# =====================================================
# Delete File
# =====================================================

def delete_file(filepath: str):

    path = Path(filepath)

    if path.exists():

        path.unlink()


# =====================================================
# AI Greeting
# =====================================================

def greeting():

    hour = datetime.now().hour

    if hour < 12:

        period = "Good Morning"

    elif hour < 17:

        period = "Good Afternoon"

    else:

        period = "Good Evening"

    return (
        f"{period}! 👋\n\n"
        "Woof🐾, I'm Canis.\n\n"
        "Conversational Assistant for "
        "Natural Intelligence & Support.\n\n"
        "Your loyal AI crony that never keeps you waiting."
    )


# =====================================================
# Health Status
# =====================================================

def status():

    return {

        "status": "running",

        "time": current_timestamp()

    }


# =====================================================
# Log
# =====================================================

def log(message: str):

    print(

        f"[{current_timestamp()}] {message}"

    )