import asyncio
import datetime
import random
import time
from dataclasses import dataclass

from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument


@dataclass
class DataGeneratorConfig:
    """Setting for amount of data to be generated in Data Generator"""

    film_amount: int = 10_000
    user_amount: int = 50_0000
    faker: Faker = Faker()


@dataclass
class DataLoaderConfig:
    """Settings for data loader."""

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    review_amount: int = 200_000
    votes_amount: int = 500_000
    bookmarks_amount: int = 300_000


class DataGenerator:
    """Generates fake data to be inserted into Mongo Database"""

    def __init__(self, config: DataGeneratorConfig):
        self.config: DataGeneratorConfig = config
        self.faker: Faker = config.faker
        self.film_uuids: set[str] = set()
        self.user_uuids: set[str] = set()

    def generate_film_uuids(self) -> int:
        if self.film_uuids:
            self.film_uuids.clear()
        for _ in range(self.config.film_amount):
            self.film_uuids.add(self.faker.uuid4())
        return len(self.film_uuids)

    def generate_user_uuids(self) -> int:
        if self.user_uuids:
            self.user_uuids.clear()
        for _ in range(self.config.user_amount):
            self.user_uuids.add(self.faker.uuid4())
        return len(self.user_uuids)

    def generate_film_review(self, amount: int = 1):
        for _ in range(amount):
            result = dict(
                user_id=random.sample(tuple(self.user_uuids), 1)[0],
                film_id=random.sample(tuple(self.film_uuids), 1)[0],
                text=self.faker.text(),
            )
            yield result

    def generate_film_vote(self, amount: int = 1):
        for _ in range(amount):
            result = dict(
                user_id=random.sample(tuple(self.user_uuids), 1)[0],
                film_id=random.sample(tuple(self.film_uuids), 1)[0],
                rating=random.randint(0, 10),
            )
            yield result

    def generate_bookmark(self, amount: int = 1):
        for _ in range(amount):
            result = dict(
                user_id=random.sample(tuple(self.user_uuids), 1)[0],
                film_id=random.sample(tuple(self.film_uuids), 1)[0],
            )
            yield result


class DataLoader:
    """Load generated data to MongoDB cluster"""

    def __init__(self, config: DataLoaderConfig, source: DataGenerator):
        self.source: DataGenerator = source
        self.total_reviews: int = config.review_amount
        self.total_votes: int = config.votes_amount
        self.total_bookmarks: int = config.bookmarks_amount
        self.mongo: AsyncIOMotorClient = AsyncIOMotorClient(
            "mongodb://{host}:{port}".format(
                host=config.mongo_host, port=config.mongo_port
            )
        )
        self.database = self.mongo.films
        self.votes_collection = self.database.get_collection("votes")
        self.reviews_collection = self.database.get_collection("reviews")
        self.bookmark_collection = self.database.get_collection("bookmarks")
        self._loop = asyncio.get_event_loop()

    def start(self):
        self._schedule_tasks()

    def _schedule_tasks(self):
        self._loop.create_task(self.load_film_reviews())
        self._loop.create_task(self.load_film_votes())
        self._loop.create_task(self.load_user_bookmarks())

    async def load_film_reviews(self) -> None:
        start = time.time()
        reviews = self.source.generate_film_review(amount=self.total_reviews)
        for review in reviews:
            filtered = {"user_id": review["user_id"], "movie_id": review["film_id"]}
            upserted = {
                "user_id": review["user_id"],
                "movie_id": review["film_id"],
                "text": review["text"],
                "timestamp": datetime.datetime.now(),
            }
            try:
                await self.reviews_collection.find_one_and_replace(
                    filtered,
                    upserted,
                    projection={"_id": False},
                    return_document=ReturnDocument.AFTER,
                    upsert=True,
                )
            except Exception as e:
                raise Exception(f"Exception {e}")
        duration = time.time() - start
        print(
            "Uploaded {} reviews: {:.2f} seconds - {} per second".format(
                self.total_reviews, duration, int(self.total_reviews / duration)
            )
        )

    async def load_film_votes(self) -> None:
        start = time.time()
        votes = self.source.generate_film_vote(amount=self.total_votes)
        for vote in votes:
            filtered = {"user_id": vote["user_id"], "movie_id": vote["film_id"]}
            upserted = {
                "user_id": vote["user_id"],
                "movie_id": vote["film_id"],
                "rating": vote["rating"],
            }
            try:
                await self.votes_collection.find_one_and_replace(
                    filtered,
                    upserted,
                    projection={"_id": False},
                    return_document=ReturnDocument.AFTER,
                    upsert=True,
                )
            except Exception as e:
                raise Exception(f"Exception {e}")
        duration = time.time() - start
        print(
            "Uploaded {} votes: {:.2f} seconds - {} per second".format(
                self.total_votes, duration, int(self.total_votes / duration)
            )
        )

    async def load_user_bookmarks(self) -> None:
        start = time.time()
        bookmarks = self.source.generate_bookmark(amount=self.total_bookmarks)
        for bookmark in bookmarks:
            existing_bookmark = await self.bookmark_collection.find_one(
                {
                    "$and": [
                        {"movie_id": bookmark["film_id"]},
                        {"user_id": bookmark["user_id"]},
                    ]
                }
            )
            if not existing_bookmark:
                await self.bookmark_collection.insert_one(
                    {"user_id": bookmark["user_id"], "movie_id": bookmark["film_id"]}
                )
        duration = time.time() - start
        print(
            "Uploaded {} bookmarks: {:.2f} seconds - {} per second".format(
                self.total_bookmarks, duration, int(self.total_bookmarks / duration)
            )
        )


class LoadManager:
    """Management of data generation and loading process."""

    def __init__(self):
        self.generator = DataGenerator(DataGeneratorConfig())
        self.uploader = DataLoader(DataLoaderConfig(), self.generator)

    def start(self):
        self.generator.generate_user_uuids()
        self.generator.generate_film_uuids()
        self.uploader.start()


def main():
    try:
        loop = asyncio.get_event_loop()
        app = LoadManager()
        app.start()
        loop.run_forever()
    except KeyboardInterrupt:
        print("Stopping event loop")
        loop.stop()


if __name__ == "__main__":
    main()
