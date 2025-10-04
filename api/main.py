from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.auth.login import router as login_router
from routes.auth.register import router as register_router
from routes.algo import router as algo_router
from db.session import connect_db, disconnect_db

client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield  
    await disconnect_db()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Routers
app.include_router(register_router, prefix="/register", tags=["Login"])
app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(algo_router, prefix="/algo", tags=["Algo"])