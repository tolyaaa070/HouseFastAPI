from .database import Base
from sqlalchemy import ForeignKey,String,Integer,DateTime,Text,Enum, Boolean, DECIMAL
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from typing import Optional,List
from enum import Enum as PY_enum

class ROLE_CHOICES(str , PY_enum):
    seller = 'seller'
    buyer = 'bayer'

class UserProfile(Base):
    __tablename__ = 'userprofile'

    id : Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[ROLE_CHOICES] = mapped_column(Enum(ROLE_CHOICES))
    password: Mapped[str] = mapped_column(String, nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    seller_property : Mapped[List['Property']] = relationship('Property' , back_populates='seller',
                                                           cascade='all , delete-orphan')
    author_reviews : Mapped[List['Reviews']] = relationship('Reviews' , back_populates='author',
                                                            cascade='all , delete-orphan')
    user_token : Mapped[List['RefreshToken']] = relationship('RefreshToken' , back_populates='user',
                                                             cascade='all , delete-orphan')

    def __repr__(self):
        return f'{self.first_name} , {self.last_name}'

class RefreshToken(Base):
    __tablename__= 'refresh_token'

    id : Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user : Mapped[UserProfile] = relationship(UserProfile , back_populates='user_token')
    token : Mapped[str] = mapped_column(String , nullable=False)
    create_date : Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)

class PROPERTY_TYPE_CHOICES(str , PY_enum):
    Apartment = 'Apartment'
    House = 'House'
    Office = 'Office'
    Plot = 'Plot'
    Garage = 'Garage'

class CONDITION_CHOICES(str , PY_enum):
      нормально = 'нормально'
      хорошо = 'хорошо'
      супер = 'супер'

class Property(Base):
    __tablename__ = 'property'

    id : Mapped[int] = mapped_column(Integer, autoincrement=True , primary_key=True)
    title : Mapped[str] = mapped_column(String)
    description :Mapped[str] = mapped_column(Text)
    property_type: Mapped[PROPERTY_TYPE_CHOICES] = mapped_column(Enum(PROPERTY_TYPE_CHOICES))
    district : Mapped[str | None] = mapped_column(String, nullable=True)
    address : Mapped[str] = mapped_column(String)
    area : Mapped[str| None] = mapped_column(String, nullable=True)
    price : Mapped[float] = mapped_column(DECIMAL(10 , 2))
    rooms : Mapped[int] = mapped_column(Integer)
    floor : Mapped[int] = mapped_column(Integer)
    total_floors :Mapped[int] = mapped_column(Integer,  nullable=True)
    condition : Mapped[CONDITION_CHOICES] = mapped_column(Enum(CONDITION_CHOICES))
    created_date : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    documents: Mapped[bool|None] = mapped_column(Boolean, nullable=True)
    seller_id : Mapped[int] = mapped_column(ForeignKey('userprofile.id'), unique=True)
    seller : Mapped[UserProfile] = relationship(UserProfile, back_populates='seller_property')
    image : Mapped[str | None] = mapped_column(String , nullable=True)
    property_reviews : Mapped[List['Reviews']] = relationship('Reviews' , back_populates='property',
                                                              cascade='all, delete-orphan')
    def __repr__(self):
        return f'{self.seller}'

class Reviews(Base):
    __tablename__= 'reviews'

    id : Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    author_id : Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    author : Mapped[UserProfile] = relationship(UserProfile, back_populates='author_reviews')
    property_id : Mapped[int] = mapped_column(ForeignKey('property.id'))
    property : Mapped[Property] = relationship(Property, back_populates='property_reviews')
    comment : Mapped[str | None] = mapped_column(Text, nullable=True)
    stars : Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_date : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.property} , {self.author}'