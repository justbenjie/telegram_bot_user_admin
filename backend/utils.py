import json
from .db import SessionLocal
from . import models, schemas


def parse_admins_id(FILE_NAME):

    with open(FILE_NAME) as file:
        data = json.load(file)
        admins = data["admins"]

    return admins


def add_admins(FILE_NAME):

    ids = parse_admins_id(FILE_NAME)

    def create_admin_model(id):
        return models.Admin(**{"user_id": id})

    admins = map(create_admin_model, ids)

    db = SessionLocal()
    for admin in admins:
        try:
            db.add_all(admin)
            db.commit()
        except:
            print(f"admin with id {admin.user_id} already exists")
    db.close()
