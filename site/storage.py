from abc import ABC, abstractmethod
from mongo import MongoDatabase

class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass


class MongoStorage(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabase()
    def store(self, data, collection, *args):
        print(self.mongo.database.get_collection(collection).find_one())

class FileStorage(StorageAbstract):
    pass


m = MongoStorage()
m.store("salam", "customers")