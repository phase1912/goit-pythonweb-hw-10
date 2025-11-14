from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate, ContactUpdate
from app.domain.contact import Contact


class ContactAlreadyExistsError(Exception):
    pass


class ContactNotFoundError(Exception):
    pass


class ContactService:
    def __init__(self, db: Session):
        self.repository = ContactRepository(db)

    def create_contact(self, contact_data: ContactCreate) -> Contact:
        if self.repository.exists_by_email(contact_data.email):
            raise ContactAlreadyExistsError(
                f"Contact with email {contact_data.email} already exists"
            )
        return self.repository.create(contact_data)

    def get_contact(self, contact_id: int) -> Contact:
        contact = self.repository.get_by_id(contact_id)
        if not contact:
            raise ContactNotFoundError(f"Contact with ID {contact_id} not found")
        return contact

    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        return self.repository.get_by_email(email)

    def get_all_contacts(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Contact], int]:
        return self.repository.get_all(skip, limit)

    def search_contacts(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Contact], int]:
        if not query or not query.strip():
            return self.get_all_contacts(skip, limit)
        return self.repository.search(query.strip(), skip, limit)

    def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        if days < 1 or days > 365:
            raise ValueError("Days must be between 1 and 365")
        return self.repository.get_upcoming_birthdays(days)

    def update_contact(
        self,
        contact_id: int,
        contact_data: ContactUpdate
    ) -> Contact:
        existing_contact = self.repository.get_by_id(contact_id)
        if not existing_contact:
            raise ContactNotFoundError(f"Contact with ID {contact_id} not found")

        if contact_data.email and contact_data.email != existing_contact.email:
            if self.repository.exists_by_email(contact_data.email, exclude_id=contact_id):
                raise ContactAlreadyExistsError(
                    f"Contact with email {contact_data.email} already exists"
                )

        updated_contact = self.repository.update(contact_id, contact_data)
        if not updated_contact:
            raise ContactNotFoundError(f"Contact with ID {contact_id} not found")
        return updated_contact

    def delete_contact(self, contact_id: int) -> bool:
        success = self.repository.delete(contact_id)
        if not success:
            raise ContactNotFoundError(f"Contact with ID {contact_id} not found")
        return True

