import functools
from config.cache_conf import get_json_cache, set_cache
from typing import List, Dict, Any, Callable, Optional
from fastapi.encoders  import jsonable_encoder
from models.news import News
from schemas.base import NewsItemBase

# 键名
CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX ="newsList:"


# 对分类添加redis缓存功能
def cache_categories(expire: int = 7200):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # 1. 尝试从缓存获取
            cached = await get_json_cache(CATEGORIES_KEY)
            if cached:
                return cached

            # 2. 执行原函数获取数据
            result = await func(*args, **kwargs)

            # 3. 序列化并写入缓存
            if result:
                data_to_cache = jsonable_encoder(result)
                await set_cache(CATEGORIES_KEY, data_to_cache, expire)

            return result
        return wrapper
    return decorator



# 写入缓存
async def set_cache_news_list(category_id: Optional[int], skip: int, limit: int, news_list: List[Dict[str, Any]],expire: int = 7200):
    category_part = category_id if category_id is not None else "news_all"
    key = f'{NEWS_LIST_PREFIX}{category_part}:{skip}:{limit}'
    return await set_cache(key, news_list, expire)

# 读取
async def get_cached_news_list(category_id: Optional[int], skip: int, limit: int):
    category_part = category_id if category_id is not None else "news_all"
    key = f'{NEWS_LIST_PREFIX}{category_part}:{skip}:{limit}'
    return await get_json_cache(key)

# 对分类列表添加redis缓存功能
def cache_news_list(expire: int = 7200):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(db, *args, **kwargs):
            # 1. 尝试从缓存获取
            cached = await get_cached_news_list(*args, **kwargs)
            if cached:
                return [News(**item) for item in cached]

            # 2. 执行原函数获取数据
            result = await func(db, *args, **kwargs)

            # 3. 序列化并写入缓存
            if result:
                # 把orm转化为字典存入
                news_data = [NewsItemBase.model_validate(item).model_dump(mode='json',by_alias=False) for item in result]
                await set_cache_news_list(news_list= news_data, expire= expire, *args, **kwargs)

            return result
        return wrapper
    return decorator