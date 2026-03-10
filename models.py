import os
import re
from datetime import datetime
from typing import Generator

from sqlalchemy import (Column, Date, DateTime, DECIMAL, Enum, Float, ForeignKey,
                        Integer, String, Boolean, JSON, create_engine, text)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# ---------------------------------------------------------------------------
# Database URL handling (with auto‑fix for DO / async prefixes)
# ---------------------------------------------------------------------------
_default_url = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))

# Replace known async prefixes with sync driver
if _default_url.startswith("postgresql+asyncpg://"):
    _default_url = _default_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _default_url.startswith("postgres://"):
    _default_url = _default_url.replace("postgres://", "postgresql+psycopg://")

# Determine if SSL is needed (non‑localhost & non‑sqlite)
_use_ssl = False
if not _default_url.startswith("sqlite") and "localhost" not in _default_url and "127.0.0.1" not in _default_url:
    _use_ssl = True

_connect_args = {"sslmode": "require"} if _use_ssl else {}

engine = create_engine(_default_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()

# ---------------------------------------------------------------------------
# Helper – dependency for FastAPI routes
# ---------------------------------------------------------------------------
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Table name prefix – "ss_" for SmartSpend
# ---------------------------------------------------------------------------
TABLE_PREFIX = "ss_"

# ---------------------------------------------------------------------------
# SQLAlchemy models (minimal set needed for demo)
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = f"{TABLE_PREFIX}users"
    user_id = Column(String, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    categories = relationship("Category", back_populates="user")

class Category(Base):
    __tablename__ = f"{TABLE_PREFIX}categories"
    category_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.user_id"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    color_code = Column(String(7), default="#000000")
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    # Relationships
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = f"{TABLE_PREFIX}transactions"
    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.user_id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    transaction_date = Column(Date, nullable=False)
    description = Column(String(255))
    category_id = Column(String, ForeignKey(f"{TABLE_PREFIX}categories.category_id"), nullable=True)
    is_pending = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class Budget(Base):
    __tablename__ = f"{TABLE_PREFIX}budgets"
    budget_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.user_id"), nullable=False)
    target_amount = Column(DECIMAL(10, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget_type = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))

class AIInsight(Base):
    __tablename__ = f"{TABLE_PREFIX}ai_insights"
    insight_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.user_id"), nullable=False)
    insight_content = Column(JSON, nullable=False)
    insight_type = Column(String(20), nullable=False)
    generated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    expires_at = Column(DateTime)

class AIRecommendation(Base):
    __tablename__ = f"{TABLE_PREFIX}ai_recommendations"
    recommendation_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.user_id"), nullable=False)
    recommendation_content = Column(JSON, nullable=False)
    recommendation_type = Column(String(20), nullable=False)
    generated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    expires_at = Column(DateTime)
