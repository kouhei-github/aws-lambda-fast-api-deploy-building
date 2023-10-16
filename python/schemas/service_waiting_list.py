from pydantic import BaseModel
from .sales_target import SalesTargetRelateUser

class ServiceWaitingList(BaseModel):
    summarize: str
    is_selected: bool
    company_id: int

class ServiceWaitingListTargetRelateUser(BaseModel):
    id: int
    summarize: str
    is_selected: bool
    company_id: int
    sales_targets: SalesTargetRelateUser
