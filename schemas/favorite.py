from datetime import datetime
from schemas.base import NewsItemBase
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


# 检查新闻收藏状态响应参数
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

# 请求收藏
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")



# 收藏接口里的news类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(..., alias="favoriteId")
    favorite_time: datetime = Field(..., alias="favoriteTime")

# 收藏列表接口
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(..., alias="hasMore")


    model_config = ConfigDict(
        populate_by_name= True,
        from_attributes= True
    )