import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt():
    return bcrypt.gensalt().decode()


def verify_password(combined_passsword, hashed_password):
    return pwd_context.verify(combined_passsword, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
