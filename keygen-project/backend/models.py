from pydantic import BaseModel

class KeyResponse(BaseModel):
    key_id: int
    stl_url: str

class ErrorResponse(BaseModel):
    detail: str
