from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.contact_service import (
    ContactService,
    ContactAlreadyExistsError,
    ContactNotFoundError
)
from app.schemas.contact import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    ContactListResponse
)

router = APIRouter(prefix="/contacts", tags=["contacts"])


def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(db)


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    service: ContactService = Depends(get_contact_service)
):
    try:
        contact = service.create_contact(contact_data)
        return contact
    except ContactAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/", response_model=ContactListResponse)
def get_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: ContactService = Depends(get_contact_service)
):
    skip = (page - 1) * page_size
    contacts, total = service.get_all_contacts(skip=skip, limit=page_size)

    return ContactListResponse(
        contacts=contacts,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/search", response_model=ContactListResponse)
def search_contacts(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: ContactService = Depends(get_contact_service)
):
    skip = (page - 1) * page_size
    contacts, total = service.search_contacts(q, skip=skip, limit=page_size)

    return ContactListResponse(
        contacts=contacts,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/birthdays", response_model=list[ContactResponse])
def get_upcoming_birthdays(
    days: int = Query(7, ge=1, le=365),
    service: ContactService = Depends(get_contact_service)
):
    try:
        contacts = service.get_upcoming_birthdays(days)
        return contacts
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    service: ContactService = Depends(get_contact_service)
):
    try:
        contact = service.get_contact(contact_id)
        return contact
    except ContactNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    service: ContactService = Depends(get_contact_service)
):
    try:
        contact = service.update_contact(contact_id, contact_data)
        return contact
    except ContactNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ContactAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    service: ContactService = Depends(get_contact_service)
):
    try:
        service.delete_contact(contact_id)
        return None
    except ContactNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

