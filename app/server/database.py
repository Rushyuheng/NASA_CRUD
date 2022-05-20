import motor.motor_asyncio
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
database = client.db
data_collection = database.get_collection("data")

def data_helper(data) -> dict:
    return{
        "key": data["key"],
        "value": data["value"]
    }

# Add a new student into to the database
async def addData(data: dict):
    # check if exist in DB

    data = await data_collection.find_one({"key": data["key"]})
    if(data):
        return None

    data = await data_collection.insert_one(data)
    new_data = await data_collection.find_one({"_id": data.inserted_id})
    return data_helper(new_data)

# Delete a student from the database
async def deleteData(key: str):
    data = await  data_collection.find_one({"key": key})
    if(data):
        await  data_collection.delete_one({"key": key})
        return True

