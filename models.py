# models.py
import datetime
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Text, ForeignKey, DateTime, Date, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # "Bağ Enerjisi" veya "Mesaj Kredisi" olarak kullanılacak alan
    bonding_energy: Mapped[int] = mapped_column(Integer, nullable=False, server_default='100')
    
    # Relationships
    images: Mapped[List["GeneratedImage"]] = relationship(back_populates="owner")
    journal_entries: Mapped[List["JournalEntry"]] = relationship(back_populates="owner")
    created_characters: Mapped[List["KaiCharacter"]] = relationship(back_populates="creator")

class KaiCharacter(Base):
    __tablename__ = "kai_characters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Karakterin hangi markaya ait olduğunu belirtir: 'PRIME' or 'RUSH'
    brand: Mapped[str] = mapped_column(String(50), nullable=False, server_default='PRIME')
    tagline: Mapped[Optional[str]] = mapped_column(String(255))
    profile_image_url: Mapped[Optional[str]] = mapped_column(String(255))
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Karakterin yaratıcısı (eğer kullanıcı tarafından yaratıldıysa)
    creator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    creator: Mapped[Optional["User"]] = relationship(back_populates="created_characters")

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("kai_characters.id"))
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    ai_response: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

class GeneratedImage(Base):
    __tablename__ = "generated_images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    image_data_base64: Mapped[str] = mapped_column(Text, nullable=False)
    # Proaktif olarak KAI tarafından üretilen "rüya" görsellerini belirtir
    is_dream: Mapped[bool] = mapped_column(Boolean, default=False)
    description_by_kai: Mapped[Optional[str]] = mapped_column(Text)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="images")

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    entry_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    
    owner: Mapped["User"] = relationship(back_populates="journal_entries")

class LearnedPoint(Base):
    __tablename__ = "learned_points"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    point_text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)