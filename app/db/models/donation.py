from sqlalchemy import Column, Integer, ForeignKey, String, Float, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Specify length for VARCHAR
    description = Column(Text, nullable=True)  # Text type doesn't require length
    photos = Column(Text, nullable=True)
    target_amount = Column(Float, nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"))
    admin = relationship("User", back_populates="donations")

