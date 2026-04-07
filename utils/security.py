from passlib.context import CryptContext

# 创建上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")


# 加密
def get_hash_password(password: str):
    return pwd_context.hash(password)


# 密码验证
def verify_password(plain_password: str, hashed_password:str) -> bool:
    """
    输入明文和密文,如果对应则返回true，否则返回false
    """
    return pwd_context.verify(secret=plain_password, hash=hashed_password)