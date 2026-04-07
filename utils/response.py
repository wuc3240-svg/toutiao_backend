from fastapi.responses import JSONResponse  # 标准化输出json
from fastapi.encoders import jsonable_encoder   # 解决fastapi里路由返回json时的转化问题


def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 将 FASTAPO, PYDANTIC, ORM 都可响应为json
    return JSONResponse(content=jsonable_encoder(content))