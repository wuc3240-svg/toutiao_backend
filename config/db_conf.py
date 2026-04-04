from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


# 数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"


# 创建引擎
async_engine = create_async_engine(
    url= ASYNC_DATABASE_URL,
    echo= True,             # 输出sql日志
    pool_size= 10,          # 连接池中持久的连接数
    max_overflow= 20        # 连接池中运行额外创建的连接数
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 创建依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        # 使用了with不用finally close