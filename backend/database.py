"""
=========================================================
CANIS AI Database
Conversational Assistant for Natural Intelligence & Support
=========================================================
"""

from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

from config import BASE_DIR


# =====================================================
# Database Path
# =====================================================

DATABASE_URL = f"sqlite:///{BASE_DIR}/canis.db"


# =====================================================
# Engine
# =====================================================

engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    }

)


# =====================================================
# Session
# =====================================================

SessionLocal = sessionmaker(

    autoflush=False,

    autocommit=False,

    bind=engine

)


# =====================================================
# Base
# =====================================================

Base = declarative_base()


# =====================================================
# Chat Table
# =====================================================

class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    role = Column(
        String(20),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# Feedback Table
# =====================================================

class Feedback(Base):

    __tablename__ = "feedback"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    rating = Column(
        Integer,
        nullable=False
    )

    comment = Column(
        Text,
        default=""
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# Uploaded Files
# =====================================================

class UploadedFile(Base):

    __tablename__ = "uploaded_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    filepath = Column(
        String(500),
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# Create Database
# =====================================================

def create_database():

    Base.metadata.create_all(bind=engine)

    print("✅ SQLite Database Ready")


# =====================================================
# Database Session
# =====================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    create_database()