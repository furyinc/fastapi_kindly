from app.db.repository.UserRepo import UserRepository
from app.db.schema.user import UserOut, UserLogin, UserRegister, TokenData
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException


class UserService:
    def __init__(self, session: Session):
        self.__userRepository = UserRepository(session=session)

    def signup(self, user_details: UserRegister) -> UserOut:
        # Check if the user already exists
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="Please Login")

        # Hash the password and prepare the data
        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_data = user_details.dict()
        user_data['hashed_password'] = hashed_password  # Rename to match the model
        user_data.pop('password')  # Remove plain password from data

        # Create the user
        created_user = self.__userRepository.create_user(user_data=user_data)

        # Return the user details
        return UserOut(
            username=created_user.username,
            email=created_user.email,
            is_admin=created_user.is_admin,
            is_verified=created_user.is_verified,
        )

    def login(self, login_details: UserLogin) -> TokenData:
        # Check if the user exists by email
        if not self.__userRepository.user_exist_by_email(email=login_details.email):
            raise HTTPException(status_code=400, detail="Please create an account")

        # Retrieve the user from the repository
        user = self.__userRepository.get_user_by_email(email=login_details.email)

        # Verify the password using the correct hashed_password field
        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.hashed_password):
            # Generate JWT token
            token = AuthHandler.sign_jwt(user_id=user.id)
            return TokenData(access_token=token)

        raise HTTPException(status_code=400, detail="Please check your Credentials")

