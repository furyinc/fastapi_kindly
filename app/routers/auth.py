from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.schema.user import UserRegister, UserLogin
from app.db.repository.UserRepo import UserRepository
from app.core.database import get_db
from app.utils.email_sender import send_email
from app.core.security.authHandler import AuthHandler
from app.utils.email_helper import generate_verification_code
from passlib.context import CryptContext

router = APIRouter()

# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define a method for hashing passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/signup")
def signup(user_data: UserRegister, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)

    # Check if email already exists
    if user_repo.user_exist_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if username already exists
    if user_repo.user_exist_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Generate verification code
    verification_code = generate_verification_code()

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user
    new_user = user_repo.create_user(
        user_data={  # Ensure the `create_user` method is expecting a dictionary
            "username": user_data.username,
            "email": user_data.email,
            "hashed_password": hashed_password,  # Store hashed password
            "verification_code": verification_code
        }
    )

    # Send email with the verification code
    subject = "Verify Your Email"
    body = f"""
    <html>
        <body>
            <h2>📬 Verify Your Email</h2>
            <p>Hello {new_user.username},</p>
            <p>To verify your email, use the following code:</p>
            <h3 style="color: #1E90FF; font-size: 40px;">{verification_code}</h3>
            <p>If you have any questions, feel free to contact us.</p>
        </body>
    </html>
    """
    send_email(to_email=new_user.email, subject=subject, body=body)

    return {"message": "User created successfully. Please verify your email."}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)

    # Authenticate user
    db_user = user_repo.authenticate_user(email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if user is verified
    if not db_user.is_verified:
        raise HTTPException(status_code=401, detail="Account not verified")

    # Generate JWT token
    token = AuthHandler.sign_jwt(user_id=db_user.id)

    return {"access_token": token, "token_type": "bearer"}
