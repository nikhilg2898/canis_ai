"""
=========================================================
CANIS AI Data Models
Conversational Assistant for Natural Intelligence & Support
=========================================================
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# =====================================================
# Chat Request
# =====================================================

class ChatRequest(BaseModel):
    """
    Request received from frontend.
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User message"
    )


# =====================================================
# Chat Response
# =====================================================

class ChatResponse(BaseModel):
    """
    Response returned to frontend.
    """

    response: str

    status: str = "success"

    timestamp: datetime = Field(
        default_factory=datetime.now
    )


# =====================================================
# Error Response
# =====================================================

class ErrorResponse(BaseModel):

    status: str = "error"

    detail: str


# =====================================================
# Upload Response
# =====================================================

class UploadResponse(BaseModel):

    filename: str

    file_size: str

    status: str = "uploaded"


# =====================================================
# Chat History Item
# =====================================================

class ChatHistoryItem(BaseModel):

    role: str

    message: str

    timestamp: datetime


# =====================================================
# Chat History Response
# =====================================================

class ChatHistoryResponse(BaseModel):

    history: List[ChatHistoryItem]


# =====================================================
# Feedback Request
# =====================================================

class FeedbackRequest(BaseModel):

    rating: int = Field(
        ge=1,
        le=5
    )

    comment: Optional[str] = ""


# =====================================================
# Health Check
# =====================================================

class HealthResponse(BaseModel):

    status: str

    app: str

    version: str