from pydantic import BaseModel, HttpUrl, field_validator
from typing import List


class URLRequest(BaseModel):
    urls: List[HttpUrl]

    @field_validator('urls')
    @classmethod
    def validate_urls_not_empty(cls, v):
        if not v:
            raise ValueError('At least one url is needed')
        return v