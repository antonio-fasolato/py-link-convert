from dataclasses import dataclass
from datetime import datetime

@dataclass()
class ApiKey:
    id: int
    timestamp: datetime
    key: str
    username: str
