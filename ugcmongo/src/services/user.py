from functools import lru_cache

from aioredis import Redis
from fastapi import Depends
from models.models import Bookmark, Bookmarks
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_mongo
from db.redis import get_redis


class UserService:
    """Class to interact with MongoDB about user bookmarks."""

    def __init__(self, redis: Redis, mongo: AsyncIOMotorClient):
        self.redis = redis
        self.mongo = mongo
        self.database = self.mongo.films
        self.collection = self.database.get_collection("bookmarks")

    async def get_user_bookmarks(self, user_id: str) -> Bookmarks or None:
        """Get user bookmarks by user_id"""
        films = await self.collection.find_one({"user_id": user_id})
        if not films:
            return None
        bookmarks = Bookmarks(user_id=user_id, movie_ids=[])
        cursor = self.collection.find({"user_id": user_id})
        for document in await cursor.to_list(length=100):
            bookmarks.movie_ids.append(document["movie_id"])
        return bookmarks

    async def add_user_bookmark(self, user_id: str, film_id: str) -> Bookmark:
        """Add bookmark to user by film_id."""
        bookmark = await self.collection.find_one(
            {"$and": [{"movie_id": film_id}, {"user_id": user_id}]}
        )
        if bookmark:
            return Bookmark(user_id=bookmark["user_id"], movie_id=bookmark["movie_id"])
        await self.collection.insert_one({"user_id": user_id, "movie_id": film_id})
        return Bookmark(user_id=user_id, movie_id=film_id)

    async def remove_user_bookmark(
        self, user_id: str, film_id: str
    ) -> Bookmark or None:
        """Find and delete user bookmark by user_id and film_id."""
        bookmark = await self.collection.find_one_and_delete(
            {"$and": [{"movie_id": film_id}, {"user_id": user_id}]},
            projection={"_id": False},
        )
        if not bookmark:
            return None
        return Bookmark(user_id=user_id, movie_id=film_id)


@lru_cache()
def get_user_service(
    redis: Redis = Depends(get_redis), mongo: AsyncIOMotorClient = Depends(get_mongo)
) -> UserService:
    return UserService(redis, mongo)
