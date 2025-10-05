from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client: AsyncIOMotorClient = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    existing_collections = await db.list_collection_names()
    if "users" not in existing_collections:
        await db.create_collection("users")
    print(f"✅ MongoDB connected : {MONGO_DB_NAME}, collections: {await db.list_collection_names()} ")

async def disconnect_db():
    global client
    client.close()
    print("❌ MongoDB disconnected.")

