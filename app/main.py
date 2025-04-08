from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.item_routes import router as item_router
from app.db.database import client 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Servidor iniciado. Conectando a MongoDB...")
    try:
        await client.admin.command("ping")  
        print("✅ Conexión exitosa")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise e
    yield
    if client:
        client.close() 
        print("MongoDB desconectado")

app = FastAPI(lifespan=lifespan)
app.include_router(item_router, prefix="/api/v1/items")