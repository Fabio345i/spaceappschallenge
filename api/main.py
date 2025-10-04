from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from routes.auth.login import router as login_router
from routes.auth.register import router as register_router
from routes.algo import router as algo_router

client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["mydb"]

    dbs = await client.list_database_names()
    print("✅ MongoDB connected. Databases found:", dbs)

    yield  
    client.close()
    print("❌ MongoDB disconnected.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Routers
app.include_router(register_router, prefix="/register", tags=["Login"])
app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(algo_router, prefix="/algo", tags=["Algo"])