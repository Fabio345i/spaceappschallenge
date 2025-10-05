from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import weather
from .routes.gibs import router as gibs_router
from .routes.algo import router as algo_router
from .routes.merra2 import router as merra2_router

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
