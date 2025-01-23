import jwt
from decouple import config
import time
from typing import Optional
from fastapi import HTTPException, Request

# Configuration
JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")


class AuthHandler:
    @staticmethod
    def sign_jwt(user_id: int) -> str:
        """
        Generate a JWT token with the user ID and expiration.
        """
        payload = {
            "id": user_id,  # Primary key
            "user_id": user_id,  # For backward compatibility
            "expires": time.time() + 900,  # Token expires in 15 minutes
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token


    @staticmethod
    def decode_jwt(token: str) -> Optional[dict]:
        """
        Decode a JWT token and return the payload if valid and not expired.
        """
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            # Check if both 'id' or 'user_id' are present
            if "id" not in decoded_token and "user_id" not in decoded_token:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token payload: Missing 'id' or 'user_id'",
                )

            if decoded_token["expires"] >= time.time():
                return decoded_token  # Return the full payload, including user_id
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def get_token(request: Request) -> str:
        """
        Extract the token from the Authorization header of a request.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=403, detail="Authorization token is missing")

        parts = auth_header.split()
        if parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=403, detail="Authorization header must start with Bearer"
            )
        if len(parts) == 1:
            raise HTTPException(status_code=403, detail="Token is missing")
        if len(parts) > 2:
            raise HTTPException(
                status_code=403, detail="Authorization header must be a single token"
            )

        return parts[1]  # Return the token



