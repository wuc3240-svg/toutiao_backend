from fastapi import APIRouter, Depends, Query, HTTPException
from crud import news
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_conf

# 创建Router实例
# prefix路由前缀
# tags分组
router = APIRouter(prefix="/api/news", tags=["news"])



@router.get("/categories", description="获取新闻分类列表")
async def get_categories(skip: int= 0, limit: int = 100, db: AsyncSession = Depends(db_conf.get_db)):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }


@router.get("/list", description="获取新闻列表")
async def get_news_list(
    category_id: int= Query(..., alias="categoryId"),
    page: int = 1,
    page_size: int = Query(10, alias="pageSize", le=100),
    db: AsyncSession = Depends(db_conf.get_db)
):
    # 分页计算，查询列表，计算总量，计算是否还有更多
    skip = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, skip, page_size)
    news_count = await news.get_news_count(db, category_id)

    if (skip + len(news_list)) < news_count:
        hasMore = True
    else:
        hasMore = False

    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": news_count,
            "hasMore": hasMore
        }
    }


@router.get("/detail", description="获取新闻详情")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(db_conf.get_db)):

    # 获取新闻数据
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(404, detail="新闻不存在")
    
    # 获取浏览量
    await news.increase_news_views(db, news_id)

    # 获取相关新闻
    related_news = await news.get_related_news(db, news_id, news_detail.category_id)

    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }