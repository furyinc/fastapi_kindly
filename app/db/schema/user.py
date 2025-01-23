from pydantic import BaseModel, EmailStr, constr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str

class TokenData(BaseModel):
    """Schema for returned token information."""
    access_token: str
    token_type: str = "Bearer"


class UserOut(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool
    is_verified: bool

    class Config:
        orm_mode = True






















# from pydantic import BaseModel, EmailStr, constr
#
# class UserRegister(BaseModel):
#     """Schema for user registration."""
#     username: str
#     email: EmailStr
#     password: constr(min_length=6)
#
# class UserLogin(BaseModel):
#     """Schema for user login."""
#     email: EmailStr
#     password: str
#
# class TokenData(BaseModel):
#     """Schema for returned token information."""
#     access_token: str
#     refresh_token: str
#     token_type: str = "Bearer"
#
# class UserOut(BaseModel):
#     """Schema for outputting user data."""
#     username: str
#     email: EmailStr
#
#     class Config:
#         orm_mode = True  # Allows mapping to ORM objects like SQLAlchemy models