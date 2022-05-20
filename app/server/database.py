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

# get all data 
async def getDatas():
    datas = []
    async for data in data_collection.find():
        datas.append(data["key"])
    return datas

# get specific key-value pair
async def getData(key:str):
    data = await  data_collection.find_one({"key": key})
    return data

# revise specific key-value pair
async def putData(key:str, data: dict):
    dataInDB = await data_collection.find_one({"key": key})
    if dataInDB:
        updatedData = await data_collection.update_one(
            {"key": key}, {"$set": {"value": data["value"]}}
        )
        return "modified"
    elif dataInDB == None:
        newData = await data_collection.insert_one(
            {"key": key,"value": data["value"]}
        )
        return "created"

# Add a new key-value pair into to the database
async def addData(data: dict):
    # check if exist in DB

    dataInDB = await data_collection.find_one({"key": data["key"]})
    if(dataInDB):
        return None

    data = await data_collection.insert_one(data)
    new_data = await data_collection.find_one({"_id": data.inserted_id})
    return data_helper(new_data)

# Delete a key-value pair from the database
async def deleteData(key: str):
    data = await  data_collection.find_one({"key": key})
    if(data):
        await  data_collection.delete_one({"key": key})
        return True
    else:
        return False

