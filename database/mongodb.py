from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

print("Mongo URI Loaded:", MONGO_URI)

client = MongoClient(MONGO_URI)

db = client["FocusFlowAI"]

users_collection = db["users"]
sessions_collection = db["sessions"]
plans_collection = db["plans"]
tasks_collection = db["tasks"]
memory_collection = db["memory"]