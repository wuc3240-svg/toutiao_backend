from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security
import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException
from utils.security import verify_password, get_hash_password

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


async def create_token(db: AsyncSession, user_id: int):
    """
    根据用户名创建或更新token
    """
    # 创建token，根据id查询token，存在则更新，不存在则添加
    token = str(uuid.uuid4())
    # 过期时间
    expires_at = datetime.now() + timedelta(days=7)

    result = await db.execute(select(UserToken).where(UserToken.user_id == user_id))
    user_token = result.scalar_one_or_none()

    if user_token:
        # 直接改就行,会自动更新
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 但是创建需要add
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)

    return token


async def autenticate_user(db: AsyncSession, username: str, password: str):
    """
    登录失败返回none,否则返回用户信息
    """
    # 查询用户名
    user = await get_user_by_username(db, username)
    if not user:
        return None
    # 验证密码
    if not security.verify_password(password, user.password):
        return None
    
    return user


async def get_user_by_token(db: AsyncSession, token: str):
    """
    传入令牌返回用户或none,先查token，再看过期，最后返回用户
    """
    result = await db.execute(select(UserToken).where(token == UserToken.token))
    user_token = result.scalar_one_or_none()

    if not user_token or user_token.expires_at < datetime.now():
        return None
    
    result = await db.execute(select(User).where(user_token.user_id == User.id))
    user = result.scalar_one_or_none()
    return user


async def update_user(db: AsyncSession, user_data: UserUpdateRequest, username: str):

    # 将user_data转为字典再解包,还要设置传入值为none时不修改
    result = await db.execute(update(User).where(username == User.username).values(**user_data.model_dump(exclude_none=True, exclude_unset=True)))

    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException("404", "用户不存在")
    # 获取更新后的信息
    return await get_user_by_username(db, username)


async def change_password(db: AsyncSession, user:User, old_password:str, new_password:str):
    """
    传入新旧密码进行验证,并且上传新密码
    """
    
    if not verify_password(old_password, new_password):
        return False
    
    hashed_password = get_hash_password(new_password)
    user.password = hashed_password

    # 防止出现seesion关闭导致的提交失败的情况
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True