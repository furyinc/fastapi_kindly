from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.repository.UserRepo import UserRepository
from app.core.security.authHandler import AuthHandler


auth_handler = AuthHandler()  # Instantiate the AuthHandler

def verify_user_is_verified(
    request: Request, db: Session = Depends(get_db)
):
    """
    Dependency to verify if a user is authenticated and verified.
    """
    # Extract the token
    token = auth_handler.get_token(request)
    # Decode the token to get user data
    token_data = auth_handler.decode_jwt(token)

    # Fetch the user from the database
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id=token_data["user_id"])

    # Check if the user is verified
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="User is not verified")

    return user  # Optionally return the user object
