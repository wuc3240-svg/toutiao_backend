from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_conf
from schemas.users import UserRequest
from crud import users
from starlette import status

router = APIRouter(
    prefix="/api/user",
    tags=["users"]
)


@router.post("/register", description="用户注册")
async def register(user_data: UserRequest, db: AsyncSession = Depends(db_conf.get_db)):
    # 检查用户是否存在，创建用户，生成令牌，响应结果
    existing_uer = await users.get_user_by_username(db, user_data.username)
    if existing_uer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已经存在")
    
    user = await users.create_user(db, user_data)
    
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }



@router.post("/login", description="用户登录")
async def login(db: AsyncSession = Depends(db_conf.get_db)):
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": 1,
                "username": "example_user",
                "nickname": "",
                "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
                "bio": "这个人很懒，什么都没留下"
            }
        }
    }


@router.get("/info", description="获取用户信息")
async def get_user_info(db: AsyncSession = Depends(db_conf.get_db)):
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": 1,
            "username": "example_user",
            "nickname": "",
            "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
            "gender": "unknown",
            "bio": "这个人很懒，什么都没留下"
        }
    }

@router.put("/update", description="更新用户信息")
async def update_user_info(db: AsyncSession = Depends(db_conf.get_db)):
    return {
        "code": 200,
        "message": "更新成功",
        "data": {
            "id": 1,
            "username": "example_user",
            "nickname": "",
            "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
            "gender": "unknown",
            "bio": "这是我的个人简介"
        }
    }

@router.put("/password", description="修改用户密码")
async def update_user_password(db: AsyncSession = Depends(db_conf.get_db)):
    return {
        "code": 200,
        "message": "密码修改成功",
        "data": ""
    }