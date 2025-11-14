from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional
import re


class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20)
    date_of_birth: date
    additional_data: Optional[str] = Field(None, max_length=500)

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError('Phone number must contain 10-15 digits')
        return cleaned

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        age_years = (date.today() - v).days / 365.25
        if age_years > 150:
            raise ValueError('Date of birth is too far in the past')
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", v):
            raise ValueError('Name can only contain letters')
        return v.title()


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    date_of_birth: Optional[date] = None
    additional_data: Optional[str] = Field(None, max_length=500)

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError('Phone number must contain 10-15 digits')
        return cleaned

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return v
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        age_years = (date.today() - v).days / 365.25
        if age_years > 150:
            raise ValueError('Date of birth is too far in the past')
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", v):
            raise ValueError('Name can only contain letters')
        return v.title()


class ContactResponse(ContactBase):
    id: int

    model_config = {"from_attributes": True}


class ContactListResponse(BaseModel):
    contacts: list[ContactResponse]
    total: int
    page: int
    page_size: int


