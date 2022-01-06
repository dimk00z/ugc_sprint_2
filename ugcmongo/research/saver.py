import asyncio
import json
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient


@dataclass
class MongoExtractorConfig:
    """Settings for mongo tester config."""

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    review_amount: int = 1_000
    votes_amount: int = 1_000
    bookmarks_amount: int = 1_000


class MongoDataExtractor:
    """Load generated data to MongoDB cluser"""

    def __init__(self, config: MongoExtractorConfig):
        self.total_reviews: int = config.review_amount
        self.total_votes: int = config.votes_amount
        self.total_bookmarks: int = config.bookmarks_amount
        self.mongo: AsyncIOMotorClient = AsyncIOMotorClient(
            "mongodb://{host}:{port}".format(
                host=config.mongo_host, port=config.mongo_port
            )
        )
        self.mongo.get_io_loop = asyncio.get_running_loop
        self.database = self.mongo.films
        self.votes_collection = self.database.get_collection("votes")
        self.reviews_collection = self.database.get_collection("reviews")
        self.bookmark_collection = self.database.get_collection("bookmarks")
        self.reviews = []
        self.votes = []
        self.bookmarks = []

    async def extract_film_reviews(self) -> None:
        cursor = self.reviews_collection.aggregate(
            [{"$sample": {"size": self.total_reviews}}]
        )
        async for doc in cursor:
            self.reviews.append(dict(user_id=doc["user_id"], movie_id=doc["movie_id"]))
        with open("reviews.json", "w") as file:
            json.dump(self.reviews, file)

    async def extract_film_votes(self) -> None:
        cursor = self.votes_collection.aggregate(
            [{"$sample": {"size": self.total_votes}}]
        )
        async for doc in cursor:
            self.votes.append(dict(user_id=doc["user_id"], movie_id=doc["movie_id"]))
        with open("votes.json", "w") as file:
            json.dump(self.votes, file)

    async def extract_user_bookmarks(self) -> None:
        cursor = self.bookmark_collection.aggregate(
            [{"$sample": {"size": self.total_bookmarks}}]
        )
        async for doc in cursor:
            self.bookmarks.append(
                dict(user_id=doc["user_id"], movie_id=doc["movie_id"])
            )
        with open("bookmarks.json", "w") as file:
            json.dump(self.bookmarks, file)


async def main(source: MongoDataExtractor):
    await source.extract_film_reviews()
    await source.extract_film_votes()
    await source.extract_user_bookmarks()


if __name__ == "__main__":
    extractor = MongoDataExtractor(MongoExtractorConfig())
    asyncio.run(main(extractor))
