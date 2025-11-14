from typing import Optional, List
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.domain.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, contact_data: ContactCreate) -> Contact:
        contact = Contact(**contact_data.model_dump())
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        return self.db.query(Contact).filter(Contact.id == contact_id).first()

    def get_by_email(self, email: str) -> Optional[Contact]:
        return self.db.query(Contact).filter(Contact.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> tuple[List[Contact], int]:
        query = self.db.query(Contact)
        total = query.count()
        contacts = query.offset(skip).limit(limit).all()
        return contacts, total

    def search(self, query: str, skip: int = 0, limit: int = 100) -> tuple[List[Contact], int]:
        search_filter = or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
        db_query = self.db.query(Contact).filter(search_filter)
        total = db_query.count()
        contacts = db_query.offset(skip).limit(limit).all()
        return contacts, total

    def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        today = date.today()
        end_date = today + timedelta(days=days)
        contacts = self.db.query(Contact).all()

        upcoming = []
        for contact in contacts:
            birthday_this_year = contact.date_of_birth.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = contact.date_of_birth.replace(year=today.year + 1)

            if today <= birthday_this_year <= end_date:
                upcoming.append(contact)

        return upcoming

    def update(self, contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]:
        contact = self.get_by_id(contact_id)
        if not contact:
            return None

        update_data = contact_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(contact, field, value)

        self.db.commit()
        self.db.refresh(contact)
        return contact

    def delete(self, contact_id: int) -> bool:
        contact = self.get_by_id(contact_id)
        if not contact:
            return False
        self.db.delete(contact)
        self.db.commit()
        return True

    def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        query = self.db.query(Contact).filter(Contact.email == email)
        if exclude_id:
            query = query.filter(Contact.id != exclude_id)
        return query.first() is not None

