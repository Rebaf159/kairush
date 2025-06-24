# database.py
import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from models import Base, User

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# Ortam değişkeninden veritabanı URL'sini oku
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL .env dosyasında bulunamadı! Lütfen .env dosyasını kontrol edin.")

# Asenkron veritabanı motorunu oluştur
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_db_and_tables():
    """Veritabanı ve tabloları (eğer mevcut değilse) oluşturur."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Her istek için bağımsız bir veritabanı oturumu sağlar."""
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """FastAPI-Users için kullanıcı veritabanı yöneticisini sağlar."""
    # Remove the 'safe' argument from the create method call
    yield SQLAlchemyUserDatabase(session, User)