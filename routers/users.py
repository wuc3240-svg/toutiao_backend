from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_conf
from models.users import User, UserChangePasswordRequest
from schemas.users import UserRequest, UserUpdateRequest
from crud import users
from starlette import status
from utils.response import success_response
from schemas.users import UserAuthResponse, UserInfoResponse
from utils.auth import get_current_user

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

    token = await users.create_token(db, user.id)

    resopnse_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=resopnse_data)
    
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }



@router.post("/login", description="用户登录")
async def login(user_data: UserRequest, db: AsyncSession = Depends(db_conf.get_db)):

    # 检查用户存在， 检查密码， 生成token， 响应结果
    user = await users.autenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    
    token = await users.create_token(db, user.id)

    resopnse_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功 ", data=resopnse_data)


@router.get("/info", description="获取用户信息")
async def get_user_info(user: User = Depends(get_current_user)):
    # 查token和用户
    return success_response(message="获取用户信息", data=UserInfoResponse.model_validate(user))


@router.put("/update", description="更新用户信息")
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):
    user = await users.update_user(db, user_data, user.username)

    return success_response(message="成功修改", data=UserInfoResponse.model_validate(user))


@router.put("/password", description="修改用户密码")
async def update_user_password(user_data: UserChangePasswordRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(db_conf.get_db)):

    res = users.change_password(db, user, user_data.old_password, user_data.new_password)
    if not res:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="设置失败请稍后再试")

    return success_response(message="修改密码成功")