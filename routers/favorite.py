from fastapi import APIRouter, Depends, Query, HTTPException
from config import db_conf
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from starlette import status

router = APIRouter(prefix="/api/favorite", tags=["favorite"])



@router.get("/check", description="检查当前新闻是否被收藏")
async def get_favorite(news_id: int = Query(..., alias="newsId"), user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):

    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)


    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorite))


@router.post("/add", description="收藏新闻")
async def add_favorite(request: FavoriteAddRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):

    result = await favorite.add_news_favorite(db, user.id, request.news_id)

    return success_response(message="收藏成功", data= result)



@router.delete("/remove", description="取消收藏新闻")
async def remove_favorite(news_id: int = Query(..., alias="newsId"), user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):

    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")

    return success_response(message="取消收藏成功")


@router.get("/list", description="获取新闻列表")
async def get_favorite_list(page: int = Query(1, ge= 1), page_size: int = Query(10, ge=1, le=100, alias="pageSize"), user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):


    rows, total = await favorite.get_favorite_list(db, user.id, page, page_size)

    favorite_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news, favorite_time, favorite_id in rows]

    has_more = total > page * page_size

    response_data = FavoriteListResponse(list=favorite_list, total=total, hasMore=has_more)

    return success_response(message="获取新闻列表成功", data=response_data)


@router.delete("/clear")
async def clear_favorite(user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):

    total = await favorite.remove_all_favorite(db, user.id)

    return success_response(message=f"清空{total}条收藏记录成功")
