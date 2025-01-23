from bcrypt import checkpw, hashpw, gensalt

class HashHelper(object):

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Ensure both inputs are bytes before comparison
        return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        # Hash the password and return it as a string
        return hashpw(plain_password.encode("utf-8"), gensalt()).decode("utf-8")



