from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Optional


class URLRequest(BaseModel):
    urls: List[HttpUrl]
    mobi: Optional[bool] = False
    
    @field_validator('urls')
    @classmethod
    def validate_urls_not_empty(cls, v):
        if not v:
            raise ValueError('Almeno una URL deve essere fornita')
        return v