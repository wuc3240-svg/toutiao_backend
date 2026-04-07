from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Header, HTTPException
from config.db_conf import get_db
from crud import users
from starlette import status


async def get_current_user(authorization: str = Header(..., alias= "Authorization"), db: AsyncSession = Depends(get_db)):
    """
    从前端的Authorization来获取用户
    """
    token = authorization.replace("Bearer ", "")
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "无效令牌")
    
    return user