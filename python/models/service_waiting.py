from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.index import Base
class ServiceWaitingList(Base):
    __tablename__ = "service_waiting_lists"
    id = Column(Integer, primary_key=True, index=True)
    summarize = Column(String(100))
    is_selected = Column(Boolean(create_constraint=False))
    company_id = Column(Integer, ForeignKey("sales_targets.id"))

    sales_targets = relationship("SalesTarget", back_populates="service_waiting_lists")
