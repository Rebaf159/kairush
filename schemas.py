# schemas.py

from fastapi_users import schemas as fastapi_users_schemas
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

# --- Mevcut Şemalar (UserRead, UserCreate vb. aynı kalıyor) ---
class UserRead(fastapi_users_schemas.BaseUser[int]):
    bonding_energy: int

class UserCreate(fastapi_users_schemas.BaseUserCreate):
    pass

class UserUpdate(fastapi_users_schemas.BaseUserUpdate):
    pass

# --- YENİ: Doğrudan Yaratılış için istek şeması ---
class DirectCreationRequest(BaseModel):
    name: str = Field(..., max_length=50)
    relationship: str = Field(..., max_length=50) # örn: "Girlfriend", "Friend", "Wife"
    personality_prompt: str = Field(..., max_length=1500)
    appearance_prompt: str = Field(..., max_length=1000)

# --- Mevcut Diğer Şemalar (CharacterRead, ChatRequest vb. aynı kalıyor) ---
class CharacterRead(BaseModel):
    id: int
    name: str
    brand: str
    tagline: Optional[str] = None
    profile_image_url: Optional[str] = None
    creator_id: Optional[int] = None

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    character_id: int

class ChatResponse(BaseModel):
    text_data: str
    audio_data: Optional[str] = None