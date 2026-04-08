import redis.asyncio as redis
import json
from typing import Any

REDIS_HOST = "localhost"    # redis主机地址
REDIS_PORT = 6379           # redis主机端口
REDIS_DB = 0                # redis数据库编号

# 创建对象
redis_client = redis.Redis(
    host= REDIS_HOST,
    port= REDIS_PORT,
    db= REDIS_DB,
    decode_responses= True  # 是否将字节解码为字符串
)


# 读取字符串
async def get_cache(key: str):
    try:
        data = await redis_client.get(key)
        return data
    except Exception as e:
        print(f"获取缓存失败:{e}")
        return None
    

# 读取列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败:{e}")
        return None



# 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):

    try:
        # 如果不是字符串,则转化
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False)   # 保留中文转字符串

        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败:{e}")
        return False
        



