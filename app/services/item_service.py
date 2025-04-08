from bson import ObjectId
from fastapi import HTTPException
from app.db.database import items_collection
from app.schemas.item_schema import Item, ItemCreate

async def create_item(item_data: ItemCreate) -> Item:
    item_dict = item_data.dict()
    result = await items_collection.insert_one(item_dict)
    created_item = await items_collection.find_one({"_id": result.inserted_id})
    return Item(**created_item)

async def get_item(item_id: str) -> Item:
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    item = await items_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return Item(**item)

async def get_all_items() -> list[Item]:
    items_cursor = items_collection.find()
    return [Item(**item) async for item in items_cursor]

async def update_item(item_id: str, item_data: ItemCreate) -> Item:
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    await items_collection.replace_one(
        {"_id": ObjectId(item_id)}, 
        item_data.dict()
    )
    updated_item = await get_item(item_id)
    return updated_item

async def delete_item(item_id: str) -> None:
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")