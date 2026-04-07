from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict



# 检查新闻收藏状态响应参数
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")