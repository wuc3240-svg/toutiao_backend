from passlib.context import CryptContext

# 创建上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")


# 加密
def get_hash_password(password: str):
    return pwd_context.hash(password)