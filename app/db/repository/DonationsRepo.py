from sqlalchemy.orm import Session
from app.db.models.donation import Donation
from fastapi import HTTPException

class DonationsRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_all_donations(self) -> list[Donation]:
        """Fetch all donation events."""
        return self.session.query(Donation).all()

    def add_donation(self, donation_data: dict, admin_id: int) -> Donation:
        """Add a new donation event to the database."""
        # Assuming donation_data["photos"] contains a list of URLs
        new_donation = Donation(
            name=donation_data["name"],
            description=donation_data["description"],
            target_amount=donation_data["target_amount"],
            photos=",".join(donation_data["photos"]),  # Store as comma-separated URLs
            admin_id=admin_id
        )
        self.session.add(new_donation)
        self.session.commit()
        self.session.refresh(new_donation)
        return new_donation





    def delete_donation(self, donation_id: int, admin_id: int):
        """Delete a donation event if the admin owns it."""
        donation = self.session.query(Donation).filter_by(id=donation_id, admin_id=admin_id).first()
        if not donation:
            raise HTTPException(status_code=404, detail="Donation not found or not authorized")
        self.session.delete(donation)
        self.session.commit()

    def update_donation(self, donation_id: int, admin_id: int, update_data: dict) -> Donation:
        """Update donation details if the admin owns it."""
        donation = self.session.query(Donation).filter_by(id=donation_id, admin_id=admin_id).first()
        if not donation:
            raise HTTPException(status_code=404, detail="Donation not found or not authorized")

        # Loop through update_data and update the fields
        for key, value in update_data.items():
            setattr(donation, key, value)

        self.session.commit()
        self.session.refresh(donation)
        return donation
























# from sqlalchemy.orm import Session
# from app.db.models.donation import Donation
# from fastapi import HTTPException
#
# class DonationsRepo:
#     def __init__(self, session: Session):
#         self.session = session
#
#
#     def get_all_donations(self) -> list[Donation]:
#         """Fetch all donation events."""
#         return self.session.query(Donation).all()
#
#
#     def add_donation(self, donation_data: dict, admin_id: int) -> Donation:
#         """Add a new donation event to the database."""
#         new_donation = Donation(
#             name=donation_data["name"],
#             description=donation_data["description"],
#             photos=",".join(donation_data["photos"]),  # Assuming a list of photo URLs
#             target_amount=donation_data["target_amount"],
#             admin_id=admin_id
#         )
#         self.session.add(new_donation)
#         self.session.commit()
#         self.session.refresh(new_donation)
#         return new_donation
#
#     def delete_donation(self, donation_id: int, admin_id: int):
#         """Delete a donation event if the admin owns it."""
#         donation = self.session.query(Donation).filter_by(id=donation_id, admin_id=admin_id).first()
#         if not donation:
#             raise HTTPException(status_code=404, detail="Donation not found or not authorized")
#         self.session.delete(donation)
#         self.session.commit()
#
#     def update_donation(self, donation_id: int, admin_id: int, update_data: dict) -> Donation:
#         """Update donation details if the admin owns it."""
#         donation = self.session.query(Donation).filter_by(id=donation_id, admin_id=admin_id).first()
#         if not donation:
#             raise HTTPException(status_code=404, detail="Donation not found or not authorized")
#
#         for key, value in update_data.items():
#             setattr(donation, key, value)
#
#         self.session.commit()
#         self.session.refresh(donation)
#         return donation
#
#
#
#     def update_donation(self, donation_id: int, admin_id: int, update_data: dict) -> Donation:
#         """Update donation details if the admin owns it."""
#         donation = self.session.query(Donation).filter_by(id=donation_id, admin_id=admin_id).first()
#         if not donation:
#             raise HTTPException(status_code=404, detail="Donation not found or not authorized")
#
#         # Loop through update_data and update the fields
#         for key, value in update_data.items():
#             setattr(donation, key, value)
#
#         self.session.commit()
#         self.session.refresh(donation)
#         return donation
