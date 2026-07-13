from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ============================================
# USER SCHEMAS
# ============================================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# CHAT SCHEMAS
# ============================================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    model: str
    timestamp: datetime


# ============================================
# CHAT HISTORY
# ============================================

class ConversationResponse(BaseModel):
    id: int
    role: str
    message: str
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# FILE UPLOAD
# ============================================

class FileResponse(BaseModel):
    id: int
    filename: str
    file_type: Optional[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True


# ============================================
# FEEDBACK
# ============================================

class FeedbackRequest(BaseModel):
    user_id: int
    message_id: Optional[int] = None
    rating: int
    comments: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    rating: int
    comments: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# STANDARD API RESPONSE
# ============================================

class APIResponse(BaseModel):
    success: bool
    message: str


# ============================================
# TOKEN
# ============================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None