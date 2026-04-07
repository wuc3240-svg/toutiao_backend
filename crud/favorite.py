from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.favorite import Favorite
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    """
    收藏了返回true，否则返回false
    """

    result = await db.execute(select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id))

    news = result.scalar_one_or_none()

    return news is not None