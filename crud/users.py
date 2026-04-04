from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.users import UserRequest
from utils import security

async def get_user_by_username(db: AsyncSession, username: str):
    """
    根据用户名查询用户是否存在，返回用户实例或者none
    
    """
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserRequest):
    """
    根据用户名创建用户
    """
    # 获取哈希加密的密码，上传
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username = user_data.username, password = hashed_password)
    db.add(user)
    await db.flush()

    return user