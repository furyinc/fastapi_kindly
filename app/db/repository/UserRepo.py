from passlib.context import CryptContext
from fastapi import HTTPException
from app.db.models.user import User

# Initialize password context for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, session):
        self.session = session

    def create_user(self, user_data: dict):
        # Use the correct field names based on the User model
        new_user = User(
            username=user_data['username'],
            email=user_data['email'],
            hashed_password=user_data['hashed_password'],
            is_admin=user_data.get('is_admin', False),
            is_verified=user_data.get('is_verified', False),
            verification_code=user_data.get('verification_code')  # Include verification code in the user creation
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def user_exist_by_email(self, email: str) -> bool:
        # Check if a user exists by email
        user = self.session.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return False

    def user_exist_by_username(self, username: str) -> bool:
        # Check if a user exists by username
        user = self.session.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(status_code=400, detail="Username already taken")
        return False

    def get_user_by_email(self, email: str) -> User:
        # Get a user by email or raise an error if not found
        user = self.session.query(User).filter_by(email=email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_id(self, user_id: int):
        if not isinstance(user_id, (int, str)):  # Check data type
            raise ValueError(f"Invalid user_id: Expected int or str, got {type(user_id).__name__}")
        return self.session.query(User).filter_by(id=user_id).first()

    def verify_user_email(self, email: str, code: int):
        # Retrieve the user based on email
        user = self.get_user_by_email(email)

        # Check if the provided code matches the user's verification code
        if user.verification_code != code:
            raise HTTPException(status_code=400, detail="Invalid verification code")

        # Update the user's verification status
        user.is_verified = True
        user.verification_code = None  # Clear the verification code after successful verification
        self.session.commit()

        return user

    def authenticate_user(self, email: str, password: str) -> User:
        # Retrieve the user by email
        user = self.get_user_by_email(email)

        # Verify the password by comparing the hash stored in the database with the input password
        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user

