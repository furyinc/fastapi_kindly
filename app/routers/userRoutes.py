from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from app.db.schema.user import UserOut
from app.core.database import get_db
from app.db.repository.UserRepo import UserRepository
from sqlalchemy.orm import Session
from app.utils.protectRoute import get_current_user
from app.db.models.user import User

router = APIRouter()


@router.get("/profile", response_model=UserOut)
def get_user_profile(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    # Debugging current_user
    print(f"Current user object: {current_user}")  # Ensure this prints a valid user object

    if not current_user or not hasattr(current_user, "id"):
        raise HTTPException(status_code=400, detail="Invalid user data")

    user_repo = UserRepository(session)
    user = user_repo.get_user_by_id(user_id=current_user.id)  # Pass scalar `id`
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user  # Return the user object




# Define a Pydantic model to parse the request body
class EmailVerificationRequest(BaseModel):
    email: str
    verification_code: int

# Email verification endpoint
@router.post("/verify-email")
def verify_email(request: EmailVerificationRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)

    # Check if the user exists by email
    user = user_repo.get_user_by_email(request.email)

    # Debugging: print both the code from the request and the code in the database
    print(f"Request Code: {request.verification_code}")
    print(f"Database Code: {user.verification_code}")

    # Verify the provided code matches the stored verification code
    if user.verification_code != request.verification_code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    # Update the user's verification status
    user.is_verified = True
    user.verification_code = None  # Clear the verification code after successful verification
    db.commit()

    return {"message": "Email verified successfully."}








