from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News
from cache import news_cache

@news_cache.cache_categories()
async def get_categories(db: AsyncSession, skip: int= 0, limit: int = 100):
    """
    获取所有分类
    """

    result = await db.execute(select(Category).offset(skip).limit(limit))
    categories = result.scalars().all()

    return categories

@news_cache.cache_news_list()
async def get_news_list(db: AsyncSession, category_id: int, skip: int= 0, limit: int = 10):
    """
    根据分类id获取新闻
    """
    result = await db.execute(select(News).where(News.category_id == category_id).offset(skip).limit(limit))
    news_list = result.scalars().all()
    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    """
    根据分类id获取新闻总数
    """
    result = await db.execute(select(func.count(News.id)).where(News.category_id == category_id))
    get_news_count = result.scalar_one()
    return get_news_count


async def get_news_detail(db: AsyncSession, news_id: int):
    """
    根据新闻id获取新闻
    """
    result = await db.execute(select(News).where(News.id == news_id))
    get_news = result.scalar_one_or_none()
    return get_news



async def increase_news_views(db: AsyncSession, news_id: int) -> bool:
    """
    更新浏览量，返回bool值，成功则true，失败则false
    """
    result = await db.execute(update(News).where(News.id == news_id).values(views = News.views + 1))
    await db.commit()   # 似乎是不用写的,get_db里存在提交,但是稳妥起见还是写吧
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    """
    获取相关新闻
    """
    # 使用order排序,浏览量最多和最新的在前面
    result = await db.execute(select(News).where(
        News.id != news_id,
        News.category_id == category_id
        ).order_by(
            News.views.desc(),
            News.publish_time.desc()
            ).limit(limit))
    related_news = result.scalars().all()

    
    # 只给前端需要的信息的写法
    return [
        {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
        } for news_detail in related_news
    ]

    return related_news