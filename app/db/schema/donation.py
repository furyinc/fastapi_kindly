from pydantic import BaseModel
from typing import Optional, List

class DonationBase(BaseModel):
    name: str
    description: str
    photos: Optional[str] = None  # URLs to photos (comma-separated, optional)
    target_amount: float




class DonationCreate(BaseModel):
    name: str
    description: str
    target_amount: float
    # photos should be handled differently for file uploads (as part of the POST request body)
    photos: List[str] = []  # This can be updated based on how you store the URLs

    class Config:
        orm_mode = True









class DonationUpdate(DonationBase):
    # Include fields that can be updated by the admin
    name: Optional[str] = None
    description: Optional[str] = None
    photos: Optional[str] = None
    target_amount: Optional[float] = None

class DonationInDB(DonationBase):
    id: int
    current_amount: float
    admin_id: int

    class Config:
        orm_mode = True  # Allows ORM objects to be converted to Pydantic models

class Donation(DonationInDB):
    admin: Optional[str]  # Admin name or other info if needed
