from sqlalchemy import Column, String, Date, Text
from app.domain.base import BaseModel


class Contact(BaseModel):
    __tablename__ = "contacts"

    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone_number = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    additional_data = Column(Text, nullable=True)
