from sqlalchemy.orm import Session
from app.db.models.user import User
from app.dependencies.admin import verify_admin_access
from app.db.repository.DonationsRepo import DonationsRepo
from app.core.database import get_db
from app.db.schema.donation import DonationCreate
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
import os
from app.db.models.donation import Donation
from pathlib import Path
from fastapi import APIRouter, Form, File, UploadFile, Depends

router = APIRouter()


# Convert UPLOAD_DIR to a Path object
UPLOAD_DIR = Path("app/static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

@router.post("/donations")
async def create_donation(
        name: str = Form(...),
        description: str = Form(...),
        target_amount: float = Form(...),
        photos: list[UploadFile] = File(...),  # Multiple files for photos
        admin: User = Depends(verify_admin_access),  # Ensure the admin is authenticated
        db: Session = Depends(get_db),  # DB session dependency
):
    # Save uploaded images and collect their URLs
    saved_images = []
    for photo in photos:
        # Use the Path object for path joining
        file_location = UPLOAD_DIR / photo.filename
        with open(file_location, "wb") as file:
            file.write(await photo.read())
        saved_images.append(f"/static/images/{photo.filename}")

    # Create a new donation record
    new_donation = Donation(
        name=name,
        description=description,
        target_amount=target_amount,
        photos=",".join(saved_images),  # Join URLs of uploaded images
        admin_id=admin.id,  # Assuming admin has `id`
    )

    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    return {"message": "Donation created successfully", "donation": new_donation}



@router.delete("/donations/{donation_id}")
def delete_donation(
    donation_id: int,
    admin: User = Depends(verify_admin_access),
    db: Session = Depends(get_db),
):
    repo = DonationsRepo(db)
    repo.delete_donation(donation_id, admin.id)
    return {"message": "Donation deleted successfully"}


@router.put("/donations/{donation_id}")
def edit_donation(
    donation_id: int,
    donation_data: dict,  # This will contain the fields that need to be updated (e.g., name, description, etc.)
    admin: User = Depends(verify_admin_access),
    db: Session = Depends(get_db),
):
    repo = DonationsRepo(db)
    updated_donation = repo.update_donation(donation_id, admin.id, donation_data)
    return {"message": "Donation updated successfully", "donation": updated_donation}



@router.get("/donations")
def get_donations(db: Session = Depends(get_db)):
    repo = DonationsRepo(db)
    return repo.get_all_donations()


