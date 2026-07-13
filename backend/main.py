"""
=========================================================
CANIS AI Backend
Conversational Assistant for Natural Intelligence & Support
=========================================================
"""

from pathlib import Path
import shutil

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from config import (
    APP_NAME,
    APP_VERSION,
    DESCRIPTION,
    ALLOWED_ORIGINS,
    UPLOAD_FOLDER,
    MAX_FILE_SIZE
)

from database import (
    create_database,
    get_db
)

from models import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse,
    UploadResponse,
    FeedbackRequest,
    HealthResponse
)

from services import (
    chat_with_canis,
    get_history,
    clear_history,
    save_uploaded_file,
    save_feedback,
    health
)
from utils import (
    allowed_file,
    validate_file_size,
    save_upload,
    readable_size
)

# ======================================================
# FastAPI App
# ======================================================

app = FastAPI(

    title=APP_NAME,

    version=APP_VERSION,

    description=DESCRIPTION

)


# ======================================================
# Database
# ======================================================

create_database()


# ======================================================
# CORS
# ======================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=ALLOWED_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ======================================================
# Root
# ======================================================

@app.get("/")
def root():

    return {

        "app": APP_NAME,

        "status": "running",

        "version": APP_VERSION

    }


# ===============================
# Health
# ======================================================

@app.get(
    "/health",
    response_model=HealthResponse
)

def health_check():

    return health()


# ======================================================
# Chat
# ======================================================

@app.post(
    "/chat",
    response_model=ChatResponse
)

def chat(

    request: ChatRequest,

    db: Session = Depends(get_db)

):

    answer = chat_with_canis(

        db,

        request.message

    )

    return ChatResponse(

        response=answer

    )


# ======================================================
# History
# ======================================================

@app.get("/history")

def history(

    db: Session = Depends(get_db)

):

    chats = get_history(db)

    return {

        "history": [

            {

                "role": c.role,

                "message": c.message,

                "timestamp": c.created_at

            }

            for c in chats

        ]

    }


# ======================================================
# Clear History
# ======================================================

@app.delete("/history")

def delete_history(

    db: Session = Depends(get_db)

):

    clear_history(db)

    return {

        "status": "success",

        "message": "Conversation cleared"

    }

# ======================================================
# Upload File
# ======================================================

@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload(

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    # Read file
    contents = await file.read()

    # Validate file size
    validate_file_size(len(contents))

    # Validate file type
    if not allowed_file(file.filename):

        raise HTTPException(

            status_code=400,

            detail="Unsupported file type."

        )

    # Reset file pointer
    await file.seek(0)

    # Save file
    filename, filepath = save_upload(

        file,

        UPLOAD_FOLDER

    )

    # Save metadata in database
    save_uploaded_file(

        db,

        filename,

        str(filepath)

    )

    return UploadResponse(

        filename=filename,

        file_size=readable_size(len(contents))

    )

# ======================================================
# Feedback
# ======================================================

@app.post("/feedback")

def feedback(

    request: FeedbackRequest,

    db: Session = Depends(get_db)

):

    save_feedback(

        db,

        request.rating,

        request.comment

    )

    return {

        "status": "success"

    }


# ======================================================
# Startup
# ======================================================

@app.on_event("startup")
def startup():

    print("=" * 55)

    print("🐺 CANIS AI Backend Started")

    print("=" * 55)

    print("App:", APP_NAME)

    print("Version:", APP_VERSION)

    print("Docs: http://127.0.0.1:8000/docs")

    print("=" * 55)