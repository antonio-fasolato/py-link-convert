from pydantic import BaseModel


class URLResponse(BaseModel):
    message: str
    url: str
    filename: str
    timestamp: str