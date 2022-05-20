from typing import Optional

from pydantic import BaseModel


class DataSchema(BaseModel):
    key: str
    value: str
