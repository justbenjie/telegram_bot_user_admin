import json
from .db import SessionLocal
from . import models, schemas


class AdminsPreloader:
    __FILE_NAME = "config.json"

    def __init__(self):
        self.admin_ids = self.__parse_admins_id(self.__FILE_NAME)

    def __parse_admins_id(self, file_name):

        with open(file_name) as file:
            data = json.load(file)
            admin_ids = data["admins"]

        return admin_ids

    def __create_user_model(self, id):
        return models.User(**{"id": id, "name": "-", "phone": "-", "gender": "-"})

    def __create_admin_model(self, id):
        return models.Admin(**{"user_id": id})

    def add_admins(self):

        users = map(self.__create_user_model, self.admin_ids)
        admins = map(self.__create_admin_model, self.admin_ids)

        for user, admin in zip(users, admins):

            try:
                db = SessionLocal()
                db.add(user)
                db.commit()
                print(f"user with id {user.id} added")
            except:
                print(f"user with id {user.id} already exists")
            finally:
                db.close()

            try:
                db = SessionLocal()
                db.add(admin)
                db.commit()
                print(f"admin with id {admin.user_id} added")
            except:
                print(f"admin with id {admin.user_id} already exists")
            finally:
                db.close()
