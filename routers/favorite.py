from fastapi import APIRouter, Depends, Query, HTTPException
from config import db_conf
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest
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