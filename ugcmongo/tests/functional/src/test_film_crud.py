from http import HTTPStatus

import pytest

from tests.functional.utils.extract import (extract_film_info,
                                            extract_film_review,
                                            extract_film_review_info,
                                            extract_film_vote, extract_message)


@pytest.mark.asyncio
async def test_film_endpoint_crud(
        make_get_request, make_post_request, make_delete_request):
    """Test film likes CRUD cycle: add, edit, delete like, check film info."""
    # Check new test film info
    response = await make_get_request('film/test-film-uuid/likes')
    message = await extract_message(response)
    assert response.status == HTTPStatus.NOT_FOUND
    assert message.detail == 'Not Found'

    # Add like to a new film
    response = await make_post_request('film/vote',
                                       json={'user_id': 'user-uuid-1',
                                             'movie_id': 'test-film-uuid',
                                             'rating': 1})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'user-uuid-1'
    assert vote.movie_id == 'test-film-uuid'
    assert vote.rating == 1

    # Check like is counted
    response = await make_get_request('film/test-film-uuid/likes')
    film_info = await extract_film_info(response)
    assert response.status == HTTPStatus.OK
    assert film_info.likes == 0
    assert film_info.dislikes == 1
    assert film_info.movie_id == 'test-film-uuid'
    assert film_info.rating == 1.0

    # Change dislike to like
    response = await make_post_request('film/vote',
                                       json={'user_id': 'user-uuid-1',
                                             'movie_id': 'test-film-uuid',
                                             'rating': 10})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'user-uuid-1'
    assert vote.movie_id == 'test-film-uuid'
    assert vote.rating == 10

    # Check change is counted
    response = await make_get_request('film/test-film-uuid/likes')
    film_info = await extract_film_info(response)
    assert response.status == HTTPStatus.OK
    assert film_info.likes == 1
    assert film_info.dislikes == 0
    assert film_info.movie_id == 'test-film-uuid'
    assert film_info.rating == 10.0

    # Add one more like from another user
    response = await make_post_request('film/vote',
                                       json={'user_id': 'user-uuid-2',
                                             'movie_id': 'test-film-uuid',
                                             'rating': 5})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'user-uuid-2'
    assert vote.movie_id == 'test-film-uuid'
    assert vote.rating == 5

    # Check average rating is calculated right
    response = await make_get_request('film/test-film-uuid/likes')
    film_info = await extract_film_info(response)
    assert response.status == HTTPStatus.OK
    assert film_info.likes == 2
    assert film_info.dislikes == 0
    assert film_info.movie_id == 'test-film-uuid'
    assert film_info.rating == 7.5

    # Add like to another film
    response = await make_post_request('film/vote',
                                       json={'user_id': 'user-uuid-1',
                                             'movie_id': 'test-film-uuid2',
                                             'rating': 3})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'user-uuid-1'
    assert vote.movie_id == 'test-film-uuid2'
    assert vote.rating == 3

    # Check another film has right rating
    response = await make_get_request('film/test-film-uuid2/likes')
    film_info = await extract_film_info(response)
    assert response.status == HTTPStatus.OK
    assert film_info.likes == 0
    assert film_info.dislikes == 1
    assert film_info.movie_id == 'test-film-uuid2'
    assert film_info.rating == 3.0

    # Remove last vote
    response = await make_delete_request('film/vote',
                                         json={'user_id': 'user-uuid-1',
                                               'movie_id': 'test-film-uuid2'})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'user-uuid-1'
    assert vote.movie_id == 'test-film-uuid2'
    assert vote.rating == 3

    # Check no likes at last film
    response = await make_get_request('film/test-film-uuid2/likes')
    message = await extract_message(response)
    assert response.status == HTTPStatus.NOT_FOUND
    assert message.detail == 'Not Found'

    # Remove votes from first film
    response = await make_delete_request('film/vote',
                                         json={'user_id': 'user-uuid-1',
                                               'movie_id': 'test-film-uuid'})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'user-uuid-1'
    assert vote.movie_id == 'test-film-uuid'
    assert vote.rating == 10

    # Check film info has changed right
    response = await make_get_request('film/test-film-uuid/likes')
    film_info = await extract_film_info(response)
    assert response.status == HTTPStatus.OK
    assert film_info.likes == 1
    assert film_info.dislikes == 0
    assert film_info.movie_id == 'test-film-uuid'
    assert film_info.rating == 5.0

    # Remove vote
    response = await make_delete_request('film/vote',
                                         json={'user_id': 'user-uuid-2',
                                               'movie_id': 'test-film-uuid'})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'user-uuid-2'
    assert vote.movie_id == 'test-film-uuid'
    assert vote.rating == 5

    # Check no likes at last film
    response = await make_get_request('film/test-film-uuid/likes')
    message = await extract_message(response)
    assert response.status == HTTPStatus.NOT_FOUND
    assert message.detail == 'Not Found'


@pytest.mark.asyncio
async def test_film_review_endpoint_crud(
        make_get_request, make_post_request, make_delete_request):
    # Check new review - not found
    response = await make_post_request('film/review/info',
                                       json={'user_id': 'test-user-uuid',
                                             'movie_id': 'test-film-uuid'})
    message = await extract_message(response)
    assert response.status == HTTPStatus.NOT_FOUND
    assert message.detail == 'Not Found'

    # Add review to film
    response = await make_post_request('film/review',
                                       json={'user_id': 'test-user-uuid',
                                             'movie_id': 'test-film-uuid',
                                             'text': 'lorem ipsum'})
    review = await extract_film_review(response)
    assert review.user_id == 'test-user-uuid'
    assert review.movie_id == 'test-film-uuid'
    assert review.text == 'lorem ipsum'

    # Check full review info
    response = await make_post_request('film/review/info',
                                       json={'user_id': 'test-user-uuid',
                                             'movie_id': 'test-film-uuid'})
    review = await extract_film_review_info(response)
    assert review.user_id == 'test-user-uuid'
    assert review.movie_id == 'test-film-uuid'
    assert review.text == 'lorem ipsum'
    assert review.timestamp
    assert review.rating is None

    # Add vote to film
    response = await make_post_request('film/vote',
                                       json={'user_id': 'test-user-uuid',
                                             'movie_id': 'test-film-uuid',
                                             'rating': 7})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'test-user-uuid'
    assert vote.movie_id == 'test-film-uuid'
    assert vote.rating == 7

    # Check full review info with new vote
    response = await make_post_request('film/review/info',
                                       json={'user_id': 'test-user-uuid',
                                             'movie_id': 'test-film-uuid'})
    review = await extract_film_review_info(response)
    assert review.user_id == 'test-user-uuid'
    assert review.movie_id == 'test-film-uuid'
    assert review.text == 'lorem ipsum'
    assert review.timestamp
    assert review.rating == 7

    # Delete review
    response = await make_delete_request('film/review',
                                         json={'user_id': 'test-user-uuid',
                                               'movie_id': 'test-film-uuid'})
    review = await extract_film_review(response)
    assert review.user_id == 'test-user-uuid'
    assert review.movie_id == 'test-film-uuid'
    assert review.text == 'lorem ipsum'

    # Check review is deleted
    response = await make_post_request('film/review/info',
                                       json={'user_id': 'test-user-uuid',
                                             'movie_id': 'test-film-uuid'})
    message = await extract_message(response)
    assert response.status == HTTPStatus.NOT_FOUND
    assert message.detail == 'Not Found'

    # Remove vote
    response = await make_delete_request('film/vote',
                                         json={'user_id': 'test-user-uuid',
                                               'movie_id': 'test-film-uuid'})
    vote = await extract_film_vote(response)
    assert vote.user_id == 'test-user-uuid'
    assert vote.movie_id == 'test-film-uuid'
    assert vote.rating == 7
