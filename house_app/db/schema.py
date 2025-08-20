from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .model import CONDITION_CHOICES, ROLE_CHOICES,PROPERTY_TYPE_CHOICES
from datetime import datetime

class UserProfileSchema(BaseModel):
    id : int
    first_name : str
    last_name : str
    username : str
    email : EmailStr
    phone_number : Optional[str]
    role : ROLE_CHOICES
    password : str
    create_date : datetime

    class Config:
        from_attributes = True

class UserProfileCreateSchema(BaseModel):
    first_name : str
    last_name : str
    username : str
    email : EmailStr
    age : Optional[int] = None
    phone_number : Optional[str]
    role : ROLE_CHOICES
    password : str

    class Config:
        from_attributes = True

class UserProfileLoginSchema(BaseModel):
    username : str
    password : str
    class Config:
        from_attributes = True

class PropertyListSchema(BaseModel):
    id : int
    title: str
    description : str
    property_type : PROPERTY_TYPE_CHOICES
    district : str
    address : str
    area : str | None
    price : float
    rooms : int
    floor : int
    total_floor : int
    condition : CONDITION_CHOICES
    documents : bool | None
    seller_id : int
    image : str
    created_date : datetime

    class Config:
        from_attributes = True

class PropertyCreateSchema(BaseModel):
    title: str
    description : str
    property_type : PROPERTY_TYPE_CHOICES
    district : str
    address : str
    area : str | None
    price : float
    rooms : int
    floor : int
    total_floors : int
    condition : CONDITION_CHOICES
    documents : bool | None
    seller_id : int
    image : str

    class Config:
        from_attributes = True


class ReviewsCreateSchema(BaseModel):
    author_id : int
    property_id : int
    comment : str | None
    stars : str
    class Config:
        from_attributes = True


class ReviewsSchema(BaseModel):
    id: int
    author_id : int
    property_id : int
    comment : str | None
    stars :  int
    created_date : datetime
    class Config:
        from_attributes = True
