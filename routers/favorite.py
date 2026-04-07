from fastapi import APIRouter, Depends, Query
from config import db_conf
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite

router = APIRouter(prefix="/api/favorite", tags=["favorite"])



@router.get("/check", description="检查当前新闻是否被收藏")
async def get_favorite(news_id: int = Query(..., alias="newsId"), user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):

    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)

    data = {
        "isFavorite": is_favorite 
    }

    return success_response(message="检查收藏状态成功", data=data)