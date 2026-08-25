from config.settings import Settings
from pymongo import MongoClient

settings = Settings()

_client = MongoClient(host=settings.MONGO_DB_URL, tz_aware= True)
_db = _client[settings.MONGO_DB_NAME]

def get_collection(collection):
    return _db[collection]

