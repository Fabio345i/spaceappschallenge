from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes.algo import router as algo_router
from api.routes.weather import rainfall
from api.db import session
from dotenv import load_dotenv
from api.routes.auth.login import router as login_router
from api.routes.auth.register import router as register_router
from api.routes.merra2 import router as merra2_router
from api.routes.algo import router as algo_router
from api.db.session import connect_db, disconnect_db
from fastapi.middleware.cors import CORSMiddleware
from api.routes.auth.favorites import router as favorite_router


from dotenv import load_dotenv
import os

load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from api.routes import weather
from .routes.gibs import router as gibs_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ici on inclut routeur météo
app.include_router(weather.router)
app.include_router(gibs_router)
app.include_router(algo_router)
app.include_router(merra2_router)

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

app.include_router(register_router, prefix="/auth", tags=["Auth"])
app.include_router(login_router, prefix="/auth", tags=["Auth"])
app.include_router(algo_router, prefix="/algo", tags=["Algo"])
app.include_router(rainfall.router, prefix="/weather", tags=["Weather"])
# app.include_router(register_router, prefix="/register", tags=["Login"])
# app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(algo_router, prefix="/algo", tags=["Algo"])
app.include_router(merra2_router, prefix="/merra2", tags=["MERRA-2"])
app.include_router(favorite_router, prefix="/auth", tags=["Favorites"])
