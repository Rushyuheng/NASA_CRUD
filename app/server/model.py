from typing import Optional

from pydantic import BaseModel


class AddDataSchema(BaseModel):
    key: str
    value: str

class PutDataSchema(BaseModel):
    value: str