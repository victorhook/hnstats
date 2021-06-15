from dataclasses import dataclass


@dataclass
class Post:
    rank: int = 0
    url: str = None
    title: str = None
    site: str = None
    score: int = 0
    user: str = None
    age: str = None
    comments: str = None
