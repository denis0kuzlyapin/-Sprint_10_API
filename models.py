from pydantic import BaseModel
from typing import Optional


# Модель для регистрации/логина
class UserAuth(BaseModel):
    email: str
    password: str


# Модель ответа при регистрации/логине
class AuthResponse(BaseModel):
    access_token: str
    refreshToken: Optional[str] = None
    user: Optional[dict] = None


# Модель для создания объявления
class CreateOfferRequest(BaseModel):
    name: str
    category: str
    condition: str
    city: str
    description: str
    price: int
    img1: Optional[str] = None
    img2: Optional[str] = None
    img3: Optional[str] = None


# Модель ответа при создании объявления
class CreateOfferResponse(BaseModel):
    id: int
    name: str
    category: str
    condition: str
    city: str
    description: str
    price: int
    owner: int
    img1: Optional[str] = None
    img2: Optional[str] = None
    img3: Optional[str] = None
    createdAt: str
    updatedAt: str
    isFavorite: Optional[str] = None
  

# Модель для редактирвоания объявления
class UpdateOfferRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    city: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
