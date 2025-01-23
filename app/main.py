# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils.init_db import create_tables
from app.routers.auth import router as AuthRouter
from app.routers.userRoutes import router as newrouter
from app.routers.donations import router as donation_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Initialize database
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=AuthRouter, tags=["auth"], prefix="/auth") #auth/login/register
app.include_router(router=newrouter, prefix="/users", tags=["users"])
app.include_router(router=donation_router, prefix="/donate")


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
