from pydantic import BaseModel


class URLResponse(BaseModel):
    message: str
    url: str
    timestamp: str