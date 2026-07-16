
from datetime import datetime

from pydantic import BaseModel

class CategorySchema(BaseModel):
    name:str
    slug:str
    description:str
class CategoryResponseSchema(BaseModel):
    id:int
    name:str
    slug:str
    description:str


class CategoryUpdateSchema(BaseModel):
    name:str
    slug:str
    description:str
class CategoryPatchSchema(BaseModel):
    name:str| None=None
    slug:str| None=None
    description:str | None=None

class CategoryBulkDeleteSchema(BaseModel):
    ids:list[int]    


