from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import weather

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

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
