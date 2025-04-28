from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.item import Item, ItemCreate

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Item]:
    """
    Retrieve items.
    """
    items = crud.item.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemCreate,
) -> Item:
    """
    Create new item.
    """
    item = crud.item.create_item(db, item=item_in)
    return item


@router.get("/{item_id}", response_model=Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
) -> Item:
    """
    Get item by ID.
    """
    item = crud.item.get_item(db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item 