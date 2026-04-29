from pydantic import BaseModel
from typing import Optional


# Модель для авторизации
class UserAuth(BaseModel):
    email: str
    password: str


# Модель для регистрации
class RegistrationUser(BaseModel):
    email: str
    password: str
    submitPassword: str


# Модель ответа на запрос авторизации
class ResponseUser(BaseModel):
    id: int
    name: str
    email: str
    avatar: Optional[str] = None
    admin: Optional[bool] = None


# Общаяодель токена
class TokenData(BaseModel):
    access_token: str


# Модель ответа на запрос регистрации
class RegistrationResponse(BaseModel):
    user: ResponseUser
    access_token: TokenData


# Модель ответа на запрос авторизации
class AuthResponse(BaseModel):
    user: ResponseUser
    token: TokenData


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
