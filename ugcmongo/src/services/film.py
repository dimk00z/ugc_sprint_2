import datetime
from functools import lru_cache

from aioredis import Redis
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from db.mongo import get_mongo
from db.redis import get_redis
from models.models import FilmInfo, FilmReview, FilmReviewInfo, FilmVote


class FilmService:
    """Class to interact with film votes (likes) and reviews."""
    def __init__(self, redis: Redis, mongo: AsyncIOMotorClient):
        self.redis = redis
        self.mongo = mongo
        self.database = mongo.films
        self.votes_collection = self.database.get_collection('votes')
        self.reviews_collection = self.database.get_collection('reviews')

    async def get_film_info(self, film_id: str) -> FilmInfo or None:
        """Get film info by film id: likes, dislikes count and avg rating."""
        film = await self.votes_collection.find_one({'movie_id': film_id})
        if not film:
            return None
        like = await self.votes_collection.count_documents(
            {'$and': [{'movie_id': film_id}, {'rating': {'$gt': 4}}]}
        )
        dislike = await self.votes_collection.count_documents(
            {'$and': [{'movie_id': film_id}, {'rating': {'$lt': 5}}]}
        )
        cursor = self.votes_collection.aggregate(
            [{'$match': {'movie_id': film_id}},
             {'$group': {'_id': 0, 'total': {'$sum': '$rating'}}}]
        )
        search_result = await cursor.to_list(length=None)
        if search_result:
            avg = search_result[0]['total'] / (like + dislike)
        else:
            avg = 0.0
        return FilmInfo(movie_id=film_id, likes=like,
                        dislikes=dislike,
                        rating=avg)

    async def upsert_film_vote(
            self, film_id: str, user_id: str, rating: int) -> FilmVote or None:
        """Update or insert user vote over film by id with rating."""
        filtered = {'user_id': user_id, 'movie_id': film_id}
        upserted = {'user_id': user_id, 'movie_id': film_id, 'rating': rating}

        upserted_vote = await self.votes_collection.find_one_and_replace(
            filtered, upserted,
            projection={'_id': False},
            return_document=ReturnDocument.AFTER,
            upsert=True
        )
        if upserted_vote:
            return FilmVote.parse_obj(upserted_vote)

    async def remove_film_vote(
            self, film_id: str, user_id: str) -> FilmVote or None:
        """Remove vote from film by user id."""
        payload = {'user_id': user_id, 'movie_id': film_id}
        removed_vote = await self.votes_collection.find_one_and_delete(
            payload, projection={'_id': False})
        if removed_vote:
            return FilmVote.parse_obj(removed_vote)

    async def get_film_review_info(
            self, film_id: str, user_id: str) -> FilmReviewInfo or None:
        """Get information about film review: text, timestamp, rating."""
        filtered = {'user_id': user_id, 'movie_id': film_id}
        review = await self.reviews_collection.find_one(filtered)
        if not review:
            return None
        votes = await self.votes_collection.find_one(filtered)
        rating = None
        if votes:
            rating = votes['rating']
        return FilmReviewInfo(movie_id=review['movie_id'],
                              user_id=review['user_id'],
                              text=review['text'],
                              timestamp=review['timestamp'],
                              rating=rating)

    async def upsert_film_review(self,
                                 film_id: str,
                                 user_id: str,
                                 text: str,
                                 timestamp: datetime.datetime) -> FilmReview:
        """Update or insert film review with text and timestamp."""
        filtered = {'user_id': user_id, 'movie_id': film_id}
        upserted = {'user_id': user_id,
                    'text': text,
                    'movie_id': film_id,
                    'timestamp': timestamp}
        upserted_review = await self.reviews_collection.find_one_and_replace(
            filtered, upserted,
            projection={'_id': False},
            return_document=ReturnDocument.AFTER,
            upsert=True
        )
        if upserted_review:
            return FilmReview.parse_obj(upserted_review)

    async def remove_film_review(
            self, film_id: str, user_id: str) -> FilmReview or None:
        """Find and remove film review by user_id and movie_id."""
        filtered = {'user_id': user_id, 'movie_id': film_id}
        removed_review = await self.reviews_collection.find_one_and_delete(
            filtered, projection={'_id': False})
        if removed_review:
            return FilmReview.parse_obj(removed_review)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        mongo: AsyncIOMotorClient = Depends(get_mongo)) -> FilmService:
    return FilmService(redis, mongo)
