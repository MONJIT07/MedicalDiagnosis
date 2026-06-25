from dotenv import load_dotenv
from pymongo import MongoClient
import os


load_dotenv()

MONGO_URL=os.getenv("MONGO_URL")
DB_NAME=os.getenv("DB_NAME","rbac-diagnosis")

client=MongoClient(MONGO_URL)
db=client[DB_NAME]


users_collection=db["users"]
reports_collection=db["reports"]
diagnosis_collection=db["diagnosis_history"]