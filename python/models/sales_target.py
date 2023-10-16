from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from config.index import Base

class SalesTarget(Base):
    __tablename__ = "sales_targets"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100))
    email = Column(String(250))
    phone = Column(String(20))
    url = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    owners = relationship("User", back_populates="sales")

    service_waiting_lists = relationship("ServiceWaitingList", back_populates="sales_targets")
