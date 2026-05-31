import os
from urllib.parse import quote_plus
from pymongo import MongoClient

username = "archisman"
password = quote_plus("rxFrYMQylJAqv22z")

MONGO_URI = f"mongodb://{username}:{password}@ac-z3ralgu-shard-00-00.rfnktuo.mongodb.net:27017,ac-z3ralgu-shard-00-01.rfnktuo.mongodb.net:27017,ac-z3ralgu-shard-00-02.rfnktuo.mongodb.net:27017/?ssl=true&replicaSet=atlas-vaml3i-shard-0&authSource=admin&appName=FocusFlowCluster"

client = MongoClient(MONGO_URI)
db = client["FocusFlowAI"]
users_collection = db["users"]
sessions_collection = db["sessions"]
plans_collection = db["plans"]
tasks_collection = db["tasks"]
memory_collection = db["memory"]