from typing import List
from dataclasses import dataclass

from models.log_url import LogUrl

@dataclass()
class HistoryResponse:
    message: str
    history: List[LogUrl]
