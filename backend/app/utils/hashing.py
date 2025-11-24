from bcrypt import checkpw, gensalt, hashpw


def get_hash(password: str) -> str:
    """Получение захешированного пароля с солью"""
    salt = gensalt()
    password_bytes = password.encode('utf-8')
    hashed_password = hashpw(password_bytes, salt)
    
    return hashed_password.decode('utf-8')


def check_pwd(pwd: str, hash_pwd: str) -> bool:
    """Проверка совпадения паролей"""
    pwd_bytes = pwd.encode('utf-8')
    hash_pwd_bytes = hash_pwd.encode('utf-8')
    return checkpw(pwd_bytes, hash_pwd_bytes)