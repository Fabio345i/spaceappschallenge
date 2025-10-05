from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes.auth.login import router as login_router
from api.routes.auth.register import router as register_router
from api.routes.merra2 import router as merra2_router
from api.routes.algo import router as algo_router
from api.db.session import connect_db, disconnect_db


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

app.include_router(register_router, prefix="/register", tags=["Login"])
app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(algo_router, prefix="/algo", tags=["Algo"])
app.include_router(merra2_router, prefix="/merra2", tags=["MERRA-2"])