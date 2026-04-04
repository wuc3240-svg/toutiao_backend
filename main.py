from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware


"""
启动
uvicorn main:app --reload



"""

# app实例
app = FastAPI()

# 跨域请求设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许访问的源
    allow_credentials= True,    # 允许携带 Cookie
    allow_methods=["*"],        # 允许的请求方法
    allow_headers=["*"]         # 允许的请求头
)

# 初始位置
@app.get("/")
async def root():
    return {"message": "Hello World!"}

# 注册路由
app.include_router(news.router)
app.include_router(users.router)