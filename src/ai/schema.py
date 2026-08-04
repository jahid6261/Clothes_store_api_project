from pydantic import BaseModel


class AIRequestSchema(BaseModel):
    prompt:str