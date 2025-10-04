from fastapi import FastAPI
from routes.auth.login import router as login_router
from routes.auth.register import router as register_router
from routes.algo import router as algo_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Include routers
app.include_router(register_router.router, prefix="/register", tags=["Login"])
app.include_router(login_router.router, prefix="/login", tags=["Login"])
app.include_router(algo_router.router, prefix="/algo", tags=["Algo"])