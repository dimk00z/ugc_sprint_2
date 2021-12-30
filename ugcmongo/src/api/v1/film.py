import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.models import (
    FilmInfo,
    FilmReview,
    FilmReviewAdd,
    FilmReviewInfo,
    FilmVote,
    FilmVoteFilter,
)

from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    "/{film_id}/likes", response_model=FilmInfo, response_model_exclude_unset=True
)
async def film_likes(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmInfo:
    film_info = await film_service.get_film_info(film_id)
    if not film_info:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return film_info


@router.post("/vote", response_model=FilmVote, response_model_exclude_unset=True)
async def upsert_film_vote(
    film_vote: FilmVote, film_service: FilmService = Depends(get_film_service)
) -> FilmVote:
    result = await film_service.upsert_film_vote(
        film_id=film_vote.movie_id, user_id=film_vote.user_id, rating=film_vote.rating
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.delete("/vote", response_model=FilmVote, response_model_exclude_unset=True)
async def remove_film_vote(
    film_vote: FilmVoteFilter, film_service: FilmService = Depends(get_film_service)
) -> FilmVote:
    result = await film_service.remove_film_vote(
        film_id=film_vote.movie_id, user_id=film_vote.user_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.post(
    "/review/info", response_model=FilmReviewInfo, response_model_exclude_unset=True
)
async def get_film_review_info(
    film_review: FilmVoteFilter, film_service: FilmService = Depends(get_film_service)
) -> FilmReview:
    result = await film_service.get_film_review_info(
        film_id=film_review.movie_id, user_id=film_review.user_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.post("/review", response_model=FilmReview, response_model_exclude_unset=True)
async def upsert_film_review(
    film_review: FilmReviewAdd, film_service: FilmService = Depends(get_film_service)
) -> FilmReview:
    result = await film_service.upsert_film_review(
        film_id=film_review.movie_id,
        user_id=film_review.user_id,
        text=film_review.text,
        timestamp=datetime.datetime.now(),
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    return result


@router.delete("/review", response_model=FilmReview, response_model_exclude_unset=True)
async def remove_film_review(
    film_review: FilmVoteFilter, film_service: FilmService = Depends(get_film_service)
) -> FilmReview:
    result = await film_service.remove_film_review(
        film_id=film_review.movie_id, user_id=film_review.user_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result
