from bson import ObjectId

from mongo.entity.usuario import User
from mongo.mongo_manager import usuario


def save_user(user: User):
    usuario.insert_one(user.user_to_dict())


def find_user_by_id(user_id) -> User:
    res = usuario.find_one({"id": user_id})
    if res is not None:
        return User(res)


def replace_user_by_id(user_id, new_user: User):
    return usuario.replace_one({"_id": ObjectId(user_id)}, new_user.user_to_dict())


def update_user_by_id(user_id, actualizacion_user: dict):
    return usuario.update_one({"_id": ObjectId(user_id)}, {"$set": actualizacion_user}, upsert=False)
