from passlib.context import CryptContext

crypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def generate_hash(password:str) -> str:
    hashed_string = crypt_context.hash(password)
    return hashed_string


def verify_hash(password:str, hashed_password:str) -> bool:
    return crypt_context.verify(password, hashed_password)