from fastapi import Header, HTTPException, Depends
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from app.db.repository.UserRepo import UserRepository
from app.core.database import get_db


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization[7:]  # Remove "Bearer "
    try:
        payload = AuthHandler.decode_jwt(token)  # Expecting a dictionary payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token decoding failed: {e}")

    # Ensure payload contains 'id' field
    if not isinstance(payload, dict) or "id" not in payload:
        raise HTTPException(status_code=400, detail="Invalid token payload: Missing 'id'")

    user_id = payload["id"]  # Extract user_id
    if not isinstance(user_id, (int, str)):  # Ensure user_id is scalar
        raise HTTPException(status_code=400, detail=f"Invalid user_id type: {type(user_id).__name__}")

    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user





