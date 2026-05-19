import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["focusflow_ai"]

sessions_collection = db["sessions"]
tasks_collection = db["tasks"]
plans_collection = db["plans"]