import datetime
from dataclasses import dataclass
from typing import Optional

from multidict import CIMultiDictProxy
from pydantic import BaseModel


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


class FilmInfo(BaseModel):
    movie_id: str
    likes: int
    dislikes: int
    rating: float


class FilmVote(BaseModel):
    user_id: str
    movie_id: str
    rating: int


class StatusMessage(BaseModel):
    detail: str


class Bookmarks(BaseModel):
    user_id: str
    movie_ids: list[str]


class Bookmark(BaseModel):
    user_id: str
    movie_id: str


class FilmReview(BaseModel):
    movie_id: str
    user_id: str
    text: str
    timestamp: datetime.datetime


class FilmReviewAdd(BaseModel):
    movie_id: str
    user_id: str
    text: str


class FilmReviewInfo(FilmReview):
    rating: Optional[int]
