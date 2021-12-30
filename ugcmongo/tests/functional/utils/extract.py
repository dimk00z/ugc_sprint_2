from tests.functional.utils.models import (Bookmark, Bookmarks, FilmInfo,
                                           FilmReview, FilmReviewInfo,
                                           FilmVote, HTTPResponse,
                                           StatusMessage)


async def extract_film_info(response: HTTPResponse) -> FilmInfo:
    info = response.body
    return FilmInfo.parse_obj(info)


async def extract_film_vote(response: HTTPResponse) -> FilmVote:
    vote = response.body
    return FilmVote.parse_obj(vote)


async def extract_message(response: HTTPResponse) -> StatusMessage:
    status = response.body
    return StatusMessage.parse_obj(status)


async def extract_bookmark(response: HTTPResponse) -> Bookmark:
    bookmark = response.body
    return Bookmark.parse_obj(bookmark)


async def extract_bookmarks(response: HTTPResponse) -> Bookmarks:
    bookmarks = response.body
    return Bookmarks.parse_obj(bookmarks)


async def extract_film_review(response: HTTPResponse) -> FilmReview:
    review = response.body
    return FilmReview.parse_obj(review)


async def extract_film_review_info(response: HTTPResponse) -> FilmReviewInfo:
    review = response.body
    return FilmReviewInfo.parse_obj(review)
