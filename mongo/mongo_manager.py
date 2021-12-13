from bson import ObjectId
from pymongo import MongoClient


class MongoManager:

    def __init__(self, collection_name, online, db):
        """
        Crea la instancia conectada a la collecion en cuestion.
        :param collection_name: nombre de la conexion
        """
        username = 'cienciaDatosUser'
        password = 'anserju'
        if online:
            self.collection = MongoClient(
                "mongodb+srv://" + username + ":" + password +
                "@practicaseguridad-0rfcm.gcp.mongodb.net/test?retryWrites=true&w=majority")[
                db][collection_name]
        else:
            self.collection = \
                MongoClient('mongodb://%s:%s@localhost:27017' % (username, password), authSource=db)[
                    db][collection_name]

    @staticmethod
    def bson_encoder(s):
        """
        Transforma el ObjectId de BSON a String, haciendo el objeto serializable
        :param s: String
        :return: String
        """
        if type(s) == ObjectId:
            return str(s)
        return s.__str__


class MongoException(Exception):
    pass


'''
    Conexiones
'''

app_collection = MongoManager('app', False, 'cienciaDatos').collection
usuario = MongoManager('usuario', False, 'cienciaDatos').collection
