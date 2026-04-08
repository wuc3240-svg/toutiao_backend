from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from models.favorite import Favorite
from models.news import News
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



async def get_favorite_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """
    获取有分页功能的收藏列，返回总量，新闻列表
    """
    # 总量
    count_result = await db.execute(select(func.count(Favorite)).where(Favorite.user_id == user_id))
    total = count_result.scalar_one_or_none()

    # 连表查询，用收藏时间排序,且分页   select(查询主体).join(联合查询类, 联合查询条件)
    skip = (page - 1) * page_size
    # result结构
    # [
    #     (新闻对象, 收藏时间, 收藏id)
    # ]
    result = await db.execute(
        select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(skip).limit(page_size)
    )
    # scalars只取元组中的第一个，取全部用all
    rows = result.all()

    return rows, total


async def remove_all_favorite(db: AsyncSession, user_id: int):

    result = await db.execute(delete(Favorite).where(Favorite.user_id == user_id))
    await db.commit()
    return result.rowcount or 0