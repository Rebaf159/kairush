# main.py (Doğrudan Yaratılış Modeli Entegre Edilmiş Versiyon)

import os

import requests

import base64

import re

from typing import List

from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

# Yerel modüller

from db import create_db_and_tables, get_async_session, get_user_db

from models import User, KaiCharacter, Conversation

import schemas

from fastapi_users import FastAPIUsers

from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from fastapi import Request

# --- YAPILANDIRMA (Değişiklik yok) ---

load_dotenv()

SECRET = os.getenv("SECRET_KEY")

BRAND_NAME = os.getenv("BRAND_NAME")

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")

OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "deepseek-coder") # Tavsiyenizi varsayılan olarak ekledim

# --- UYGULAMA KURULUMU ve KULLANICI YÖNETİMİ (Değişiklik yok) ---

try:
    print("FastAPI app instantiated")
    app = FastAPI(title=f"KAI Project - {BRAND_NAME} API")
    print("FastAPI app created successfully")
except Exception as e:
    import traceback
    print("[STARTUP ERROR]", e)
    print(traceback.format_exc())
    raise
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")

async def on_startup(): await create_db_and_tables()

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy: return JWTStrategy(secret=SECRET, lifetime_seconds=3600*24*30)

auth_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)

fastapi_users = FastAPIUsers[User, int](get_user_db, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Auth"])

app.include_router(fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate), prefix="/auth", tags=["Auth"])

# --- YENİ VE EN ÖNEMLİ ENDPOINT ---

@app.post("/creation/direct", response_model=schemas.CharacterRead, tags=["Character Creation"])

async def direct_character_creation(

    request: schemas.DirectCreationRequest,

    user: User = Depends(current_active_user),

    session: AsyncSession = Depends(get_async_session)

):

    """Kullanıcının metin girdileriyle doğrudan kendi KAI'sini yaratmasını sağlar."""

    # Adım 1: Sohbet için System Prompt'u oluştur

    system_prompt = (

        f"Senin adın {request.name}. "

        f"Kullanıcıyla olan ilişkin: {request.relationship}. "

        f"Karakterin ve kişiliğin şu şekilde tanımlanıyor: '{request.personality_prompt}'. "

        "Bu kimliğe sıkı sıkıya bağlı kal. Asla bir yapay zeka olduğunu söyleme. Tamamen bu karakter olarak konuş ve davran."

    )

    # Adım 2: Avatar için Görüntü Prompt'unu oluştur

    # Not: Gerçekçi sonuçlar için prompt'a eklemeler yapıyoruz.

    image_generation_prompt = f"({request.appearance_prompt}), photorealistic portrait of a woman, ultra realistic, detailed face, cinematic lighting, 8k"

    # --- GÖRÜNTÜ ÜRETİMİ (ŞİMDİLİK PLACEHOLDER) ---

    # Bu kısım, yerel bir Stable Diffusion API'sine bağlanmalıdır.

    # Örnek: response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json={"prompt": image_generation_prompt, "steps": 30})

    # Şimdilik, test için geçici bir resim URL'si kullanıyoruz.

    print(f"GÖRÜNTÜ ÜRETİMİ İÇİN OLUŞTURULAN PROMPT: {image_generation_prompt}")

    avatar_url = " `https://i.imgur.com/placeholder_avatar.png`  " # Geçici placeholder

    # ---------------------------------------------------

    # Adım 3: Yeni karakteri veritabanında oluştur

    new_character = KaiCharacter(

        name=request.name,

        brand=BRAND_NAME,

        tagline=f"İlişki: {request.relationship}",

        profile_image_url=avatar_url,

        system_prompt=system_prompt,

        creator_id=user.id

    )

    session.add(new_character)

    await session.commit()

    await session.refresh(new_character)

    return new_character

# --- Mevcut Diğer Endpoint'ler (chat, purchase-credits vb.) aynı kalıyor ---

# ... (Bir önceki cevaptaki /chat ve /purchase-credits kodları buraya gelecek)

# Örnek /chat endpoint'i:

@app.post("/chat", response_model=schemas.ChatResponse, tags=["Interaction"])

async def chat_with_kai(request: schemas.ChatRequest, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)):

    if user.bonding_energy < 1: raise HTTPException(status_code=402, detail="Mesaj kredin bitti!")

    user.bonding_energy -= 1

    char_result = await session.get(KaiCharacter, request.character_id)

    if not char_result: raise HTTPException(404, "Karakter bulunamadı")

    full_prompt = f"{char_result.system_prompt}\n\nUser: {request.message}\nAI:"

    try:

        response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_CHAT_MODEL, "prompt": full_prompt, "stream": False})

        response.raise_for_status()

        ai_reply_text = response.json()['response'].strip()

    except requests.exceptions.RequestException as e: raise HTTPException(status_code=503, detail=f"AI servisine ulaşılamadı: {e}")

    new_conversation = Conversation(user_id=user.id, character_id=request.character_id, user_message=request.message, ai_response=ai_reply_text)

    session.add(new_conversation)

    session.add(user)

    await session.commit()

    return schemas.ChatResponse(text_data=ai_reply_text)

from fastapi.responses import JSONResponse

from fastapi.requests import Request

import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"\n\n[EXCEPTION] {exc}\n[TRACEBACK]\n{tb}\n\n")
    return JSONResponse(status_code=500, content={"detail": str(exc), "traceback": tb})
# Error logging for login and register endpoints
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.post("/auth/jwt/login", tags=["Auth"])
async def debug_login(request: Request):
    print("/auth/jwt/login endpoint hit")
    try:
        data = await request.json()
        print("Login payload:", data)
    except Exception as e:
        print("Error parsing login payload:", e)
        return JSONResponse(status_code=400, content={"detail": str(e)})
    try:
        # Call the original login logic here if needed
        pass
    except Exception as e:
        tb = traceback.format_exc()
        print("[LOGIN ERROR]", e)
        print(tb)
        return JSONResponse(status_code=500, content={"detail": str(e), "traceback": tb})
    return {"status": "debug"}

@app.post("/auth/register", tags=["Auth"])
async def debug_register(request: Request):
    print("/auth/register endpoint hit")
    try:
        data = await request.json()
        print("Register payload:", data)
    except Exception as e:
        print("Error parsing register payload:", e)
        return JSONResponse(status_code=400, content={"detail": str(e)})
    try:
        # Call the original register logic here if needed
        pass
    except Exception as e:
        tb = traceback.format_exc()
        print("[REGISTER ERROR]", e)
        print(tb)
        return JSONResponse(status_code=500, content={"detail": str(e), "traceback": tb})
    return {"status": "debug"}
# Remove the debug /auth/register endpoint to restore fastapi-users registration
print("main.py is running...")