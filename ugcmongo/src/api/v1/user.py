from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.models import Bookmark, Bookmarks
from services.user import UserService, get_user_service

router = APIRouter()


@router.get('/{user_id}/bookmarks', response_model=Bookmarks,
            response_model_exclude_unset=True)
async def user_bookmarks(user_id: str,
                         user_service: UserService = Depends(get_user_service)
                         ) -> Bookmarks:
    bookmarks = await user_service.get_user_bookmarks(user_id)
    if not bookmarks:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return bookmarks


@router.post('/bookmark',
             response_model=Bookmark, response_model_exclude_unset=True)
async def add_bookmark(bookmark: Bookmark,
                       user_service: UserService = Depends(get_user_service)
                       ) -> Bookmark:
    result = await user_service.add_user_bookmark(
        film_id=bookmark.movie_id,
        user_id=bookmark.user_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    return result


@router.delete('/bookmark',
               response_model=Bookmark, response_model_exclude_unset=True)
async def remove_bookmark(bookmark: Bookmark,
                          user_service: UserService = Depends(get_user_service)
                          ) -> Bookmark:
    result = await user_service.remove_user_bookmark(
        film_id=bookmark.movie_id,
        user_id=bookmark.user_id
    )
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result
