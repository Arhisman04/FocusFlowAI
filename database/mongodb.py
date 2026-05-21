from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://archisman:22428126422283558340agad@focusflowcluster.rfnktuo.mongodb.net/?retryWrites=true&w=majority&appName=FocusFlowCluster"
)

db = client["focusflow"]

sessions_collection = db["sessions"]
tasks_collection = db["tasks"]
plans_collection = db["plans"]
memory_collection = db["memory"]
users_collection = db["users"]