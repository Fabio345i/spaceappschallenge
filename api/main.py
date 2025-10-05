from fastapi import FastAPI
from contextlib import asynccontextmanager
# from api.routes.auth.login import router as login_router
# from api.routes.auth.register import router as register_router
from api.routes.algo import router as algo_router
from api.routes.weather import rainfall
from api.db import session
from dotenv import load_dotenv


from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await session.connect_db()
    yield  
    await session.disconnect_db()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",  # Domaine de dev
    "http://167.160.189.194",    # Domaine de prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# app.include_router(register_router, prefix="/auth", tags=["Auth"])
# app.include_router(login_router, prefix="/auth", tags=["Auth"])
app.include_router(algo_router, prefix="/algo", tags=["Algo"])
app.include_router(rainfall.router, prefix="/weather", tags=["Weather"])
