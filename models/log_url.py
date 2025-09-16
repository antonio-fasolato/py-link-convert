from dataclasses import dataclass

@dataclass()
class LogUrl:
    id: int
    username: str
    timestamp: str
    title: str
    url: str