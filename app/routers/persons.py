from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Person
from app.schemas import PersonRequest, PersonResponse

router = APIRouter(prefix="/api/v1/persons", tags=["Person REST API operations"])


def _get_person_or_404(db: Session, person_id: int) -> Person:
    person = db.get(Person, person_id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.get("", response_model=List[PersonResponse])
def list_persons(db: Session = Depends(get_db)):
    return db.scalars(select(Person).order_by(Person.id)).all()


@router.post("", status_code=status.HTTP_201_CREATED, response_class=Response)
def create_person(request: Request, data: PersonRequest, db: Session = Depends(get_db)):
    person = Person(**data.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/api/v1/persons/{person.id}"},
    )


@router.get("/{person_id}", response_model=PersonResponse)
def get_person(person_id: int, db: Session = Depends(get_db)):
    return _get_person_or_404(db, person_id)


@router.patch("/{person_id}", response_model=PersonResponse)
def update_person(person_id: int, data: PersonRequest, db: Session = Depends(get_db)):
    person = _get_person_or_404(db, person_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(person, field, value)
    db.commit()
    db.refresh(person)
    return person


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = _get_person_or_404(db, person_id)
    db.delete(person)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
