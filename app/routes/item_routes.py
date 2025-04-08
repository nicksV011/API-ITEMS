from fastapi import APIRouter, HTTPException, status
from app.schemas.item_schema import Item, ItemCreate
from app.services.item_service import (
    create_item,
    get_item,
    get_all_items,
    update_item,
    delete_item
)

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_new_item(item: ItemCreate):
    return await create_item(item)

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return await get_item(item_id)

@router.get("/", response_model=list[Item])
async def read_all_items():
    return await get_all_items()

@router.put("/{item_id}", response_model=Item)
async def update_existing_item(item_id: str, item: ItemCreate):
    return await update_item(item_id, item)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(item_id: str):
    await delete_item(item_id)