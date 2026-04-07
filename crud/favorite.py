from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.favorite import Favorite
from schemas.favorite import FavoriteAddRequest
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    """
    收藏了返回true，否则返回false
    """

    result = await db.execute(select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id))

    news = result.scalar_one_or_none()

    return news is not None

async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    """
    根据用户id和新闻id添加收藏
    
    """

    favorite = Favorite(user_id=user_id, news_id=news_id)

    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def remove_news_favorite(db: AsyncSession, user_id:int, news_id:int):
    """
    根据用户id和新闻id取消收藏, 成功取消返回true，否则返回false
    """

    result = await db.execute(delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id))
    
    await db.commit()
    return  result.rowcount > 0