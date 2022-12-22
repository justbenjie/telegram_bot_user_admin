from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import admin, user
from .db import engine
from .preloader import AdminsPreloader


models.Base.metadata.create_all(bind=engine)

admins_preloader = AdminsPreloader()
admins_preloader.add_admins()

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
