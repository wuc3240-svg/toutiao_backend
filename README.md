# Toutiao Backend

基于 FastAPI 构建的今日头条后端 RESTful API 项目。

## 相关项目

前端项目：[xwzx-news](https://github.com/wuc3240-svg/xwzx-news.git) - 对应 Vue 前端实现

## 技术栈

- **框架**: FastAPI
- **数据库**: MySQL + SQLAlchemy（异步）+ aiomysql
- **缓存**: Redis
- **认证**: JWT Token
- **密码加密**: bcrypt
- **异步支持**: async/await

## 功能模块

### 用户模块
- `POST /api/user/register` - 用户注册
- `POST /api/user/login` - 用户登录
- `GET /api/user/info` - 获取当前用户信息（需要认证）
- `PUT /api/user/update` - 更新用户信息（需要认证）
- `PUT /api/user/password` - 修改用户密码（需要认证）

### 新闻模块
- `GET /api/news/categories` - 获取新闻分类列表
- `GET /api/news/list` - 获取新闻列表（分页，按分类筛选）
- `GET /api/news/detail` - 获取新闻详情（包含相关新闻推荐）

### 收藏模块
- `GET /api/favorite/check` - 检查新闻是否已收藏（需要认证）
- `POST /api/favorite/add` - 添加新闻收藏（需要认证）
- `DELETE /api/favorite/remove` - 取消收藏（需要认证）
- `GET /api/favorite/list` - 获取用户收藏列表（分页，需要认证）
- `DELETE /api/favorite/clear` - 清空所有收藏（需要认证）

## 项目结构

```
toutiao_backend/
├── cache/                # 缓存相关
├── config/               # 配置文件
│   ├── cache_conf.py     # Redis 配置
│   └── db_conf.py        # 数据库配置
├── crud/                 # 数据库操作
│   ├── favorite.py
│   ├── news.py
│   └── users.py
├── models/               # 数据库模型
│   ├── favorite.py
│   ├── news.py
│   └── users.py
├── routers/              # API 路由
│   ├── favorite.py
│   ├── news.py
│   └── users.py
├── schemas/              # Pydantic 模型
│   ├── base.py
│   ├── favorite.py
│   └── users.py
├── utils/                # 工具函数
│   ├── auth.py           # JWT 认证
│   ├── exception.py      # 异常定义
│   ├── exception_handlers.py # 异常处理器
│   ├── response.py       # 响应封装
│   └── security.py       # 密码加密
├── 示例数据库/            # 数据库文件
│   └── database.sql      # 完整建表语句+示例数据
├── main.py               # 应用入口
└── pyproject.toml        # 项目依赖
```

## 环境要求

- Python >= 3.12
- MySQL >= 5.7
- Redis >= 6.0

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd toutiao_backend
```

### 2. 创建虚拟环境并安装依赖

使用 uv（推荐）：

```bash
uv sync
```

使用 pip：

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

创建 MySQL 数据库：

```sql
CREATE DATABASE news_app CHARACTER SET utf8mb4;
```

然后根据需要修改 `config/db_conf.py` 中的数据库连接信息：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/news_app?charset=utf8mb4"
```

### 4. 导入数据库

项目提供了完整的示例数据库 SQL 文件，包含建表语句和示例数据，可以直接导入使用：

```bash
mysql -u username -p news_app < "示例数据库/database.sql"
```

SQL 文件包含以下数据表：
- `user` - 用户表
- `user_token` - 用户令牌表
- `news_category` - 新闻分类表
- `news` - 新闻表（包含示例新闻数据）
- `related_news` - 相关新闻关联表
- `favorite` - 收藏关系表

### 5. 配置 Redis

修改 `config/cache_conf.py` 中的 Redis 连接信息（默认 localhost:6379）

### 6. 启动服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后，访问 http://127.0.0.1:8000 即可。

## API 文档

启动服务后，可以访问以下地址查看自动生成的 API 文档：

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 配置说明

### 数据库配置

位于 `config/db_conf.py`：
- `ASYNC_DATABASE_URL`: 异步数据库连接URL
- 连接池配置：`pool_size` 和 `max_overflow`

### Redis 配置

位于 `config/cache_conf.py`：
- `REDIS_HOST`: Redis 主机地址
- `REDIS_PORT`: Redis 端口
- `REDIS_DB`: Redis 数据库编号

## API 响应格式

统一响应格式：

```json
{
  "code": 200,
  "message": "成功消息",
  "data": { ... }
}
```

错误情况会通过 HTTP 状态码和错误详情返回。

## 认证方式

- 使用 JWT Token 进行身份认证
- Token 通过请求头 `Authorization: Bearer <token>` 传递
- 需要认证的接口会在 FastAPI 文档中标注

## 开发说明

- 项目采用异步架构，所有数据库操作为异步
- Redis 缓存用于热门数据提速
- 统一异常处理，返回格式一致
- 支持 CORS 跨域请求

## 许可证

MIT
