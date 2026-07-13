# from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# import auth
import models
import schemas
import services

from database import get_db
# from config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()


# ==========================================
# Register
# ==========================================

# @router.post("/register")
# def register(
#     user: schemas.UserRegister,
#     db: Session = Depends(get_db)
# ):

#     existing_user = (
#         db.query(models.User)
#         .filter(models.User.email == user.email)
#         .first()
#     )

#     if existing_user:
#         raise HTTPException(
#             status_code=400,
#             detail="Email already registered"
#         )

#     new_user = models.User(
#         username=user.username,
#         email=user.email,
#         hashed_password=auth.hash_password(user.password)
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {
#         "message": "User registered successfully"
#     }


# ==========================================
# Login
# ==========================================

# @router.post("/login")
# def login(
#     user: schemas.UserLogin,
#     db: Session = Depends(get_db)
# ):

#     db_user = auth.authenticate_user(
#         db,
#         user.email,
#         user.password
#     )

#     if not db_user:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid email or password"
#         )

#     access_token = auth.create_access_token(
#         data={"sub": db_user.email},
#         expires_delta=timedelta(
#             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     )

#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }


# ==========================================
# Chat
# ==========================================

@router.post("/chat")
def chat(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(auth.get_current_user)
):

    return services.process_chat(
        db=db,
        # user_id=current_user.id,
        request=request
    )


# ==========================================
# History
# ==========================================

@router.get("/history")
def history(
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(auth.get_current_user)
):

    return services.get_history(
        db,
        # current_user.id
    )


# ==========================================
# Delete History
# ==========================================

@router.delete("/history/{conversation_id}")
def delete_history(
    conversation_id: int,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(auth.get_current_user)
):

    deleted = services.delete_history(
        db,
        conversation_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return {
        "message": "Conversation deleted"
    }


# ==========================================
# Feedback
# ==========================================

@router.post("/feedback")
def feedback(
    feedback: schemas.FeedbackRequest,
    db: Session = Depends(get_db)
):

    return services.save_feedback(
        db,
        feedback
    )


# ==========================================
# Health Check
# ==========================================

@router.get("/health")
def health():

    return {
        "status": "running",
        "service": "CANIS AI"
    }