from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import admin, user
from .db import engine
from .utils import add_admins

FILE_NAME = "config.json"

models.Base.metadata.create_all(bind=engine)

add_admins(FILE_NAME)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(admin.router)


@app.get("/")
def test_posts():

    return {"data": "Welcome!"}
