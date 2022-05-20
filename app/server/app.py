from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .model import DataSchema
from .database import addData

app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.post("/key", response_description="data added into the database")
async def addDataRoute(data:DataSchema):
    data = jsonable_encoder(data)
    newData = await addData(data)
    if newData == None:
        raise HTTPException(status_code = 400, detail = "key already exist")
    elif newData:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=newData)