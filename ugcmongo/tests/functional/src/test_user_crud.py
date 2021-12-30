from http import HTTPStatus

import pytest
from tests.functional.utils.extract import (
    extract_bookmark,
    extract_bookmarks,
    extract_message,
)


@pytest.mark.asyncio
async def test_user_bookmarks_endpoint_crud(
    make_get_request, make_post_request, make_delete_request
):
    """Test film likes CRUD cycle: add, edit, delete like, check film info."""
    # Check we have no user bookmarks
    response = await make_get_request("user/test-usr-uuid/bookmarks")
    message = await extract_message(response)
    assert response.status == HTTPStatus.NOT_FOUND
    assert message.detail == "Not Found"

    # Add first test bookmark
    response = await make_post_request(
        "user/bookmark",
        json={"user_id": "test-usr-uuid", "movie_id": "test-film-uuid0"},
    )
    bookmark = await extract_bookmark(response)
    assert response.status == HTTPStatus.OK
    assert bookmark.user_id == "test-usr-uuid"
    assert bookmark.movie_id == "test-film-uuid0"

    # Check bookmark has been added
    response = await make_get_request("user/test-usr-uuid/bookmarks")
    bookmarks = await extract_bookmarks(response)
    assert response.status == HTTPStatus.OK
    assert bookmarks.user_id == "test-usr-uuid"
    assert len(bookmarks.movie_ids) == 1

    # Add second test bookmark
    response = await make_post_request(
        "user/bookmark",
        json={"user_id": "test-usr-uuid", "movie_id": "test-film-uuid1"},
    )
    bookmark = await extract_bookmark(response)
    assert response.status == HTTPStatus.OK
    assert bookmark.user_id == "test-usr-uuid"
    assert bookmark.movie_id == "test-film-uuid1"

    # Check second bookmark has been added
    response = await make_get_request("user/test-usr-uuid/bookmarks")
    bookmarks = await extract_bookmarks(response)
    assert response.status == HTTPStatus.OK
    assert bookmarks.user_id == "test-usr-uuid"
    assert len(bookmarks.movie_ids) == 2

    # Remove first test bookmark from user
    response = await make_delete_request(
        "user/bookmark",
        json={"user_id": "test-usr-uuid", "movie_id": "test-film-uuid0"},
    )
    bookmark = await extract_bookmark(response)
    assert response.status == HTTPStatus.OK
    assert bookmark.user_id == "test-usr-uuid"
    assert bookmark.movie_id == "test-film-uuid0"

    # Check first bookmark has been removed
    response = await make_get_request("user/test-usr-uuid/bookmarks")
    bookmarks = await extract_bookmarks(response)
    assert response.status == HTTPStatus.OK
    assert bookmarks.user_id == "test-usr-uuid"
    assert len(bookmarks.movie_ids) == 1

    # Remove second test bookmark from user
    response = await make_delete_request(
        "user/bookmark",
        json={"user_id": "test-usr-uuid", "movie_id": "test-film-uuid1"},
    )
    bookmark = await extract_bookmark(response)
    assert response.status == HTTPStatus.OK
    assert bookmark.user_id == "test-usr-uuid"
    assert bookmark.movie_id == "test-film-uuid1"

    # Check second bookmark has been removed
    response = await make_get_request("user/test-usr-uuid/bookmarks")
    message = await extract_message(response)
    assert response.status == HTTPStatus.NOT_FOUND
    assert message.detail == "Not Found"
