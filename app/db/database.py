from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
database = client.Cluster0
items_collection = database.get_collection("items")
