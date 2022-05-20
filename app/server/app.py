from fastapi import FastAPI, HTTPException,Response,status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .model import AddDataSchema,PutDataSchema
from .database import addData,deleteData,getDatas,getData,putData

app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.get("/key", response_description="get all keys")
async def getDatasRoute():
    datas = await getDatas()
    return datas 

@app.get("/key/{key:path}", response_description="get single key-value pair")
async def getDataRoute(key: str):
    data = await getData(key)
    if data == None:
        raise HTTPException(status_code = 404, detail = "key not exist")
    elif data:
        return{data["key"]:data["value"]}

@app.post("/key", response_description="data added into the database",response_model= AddDataSchema)
async def addDataRoute(data:AddDataSchema,response: Response):
    data = jsonable_encoder(data)
    newData = await addData(data)
    if newData == None:
        raise HTTPException(status_code = 400, detail = "key already exist")
    elif newData:
        response.status_code = status.HTTP_201_CREATED
        return newData

@app.put("/key/{key:path}", response_description="revise data in the database")
async def putDataRoute(key: str,data:PutDataSchema,response: Response):
    data = jsonable_encoder(data)
    statusDB = await putData(key,data)
    if statusDB == "created":
        response.status_code = status.HTTP_201_CREATED

@app.delete("/key/{key:path}", response_description="data deleted from the database")
async def deleteDataRoute(key: str):
    deletedData = await deleteData(key)