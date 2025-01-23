from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.repository.UserRepo import UserRepository
from app.core.security.authHandler import AuthHandler


def verify_admin_access(request: Request, db: Session = Depends(get_db)):
    token = AuthHandler.get_token(request)  # Extract token
    token_data = AuthHandler.decode_jwt(token)  # Decode token

    if not token_data:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    user_id = token_data.get("id") or token_data.get("user_id")  # Access either key

    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id=user_id)

    if not user.is_admin:  # Check if the user has admin privileges
        raise HTTPException(status_code=403, detail="Access denied: Admins only")

    return user  # Return the user object if needed
