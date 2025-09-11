from dataclasses import dataclass
from pydantic import BaseModel
from typing import List


@dataclass
class URLResponse(BaseModel):
    message: str
    urls: List[str]
    filename: str
    timestamp: str
    chapters_count: int