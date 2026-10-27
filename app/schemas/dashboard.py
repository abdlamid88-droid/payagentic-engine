from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DealAuditRecord(BaseModel):
    transaction_id: str
    package_id: str
    target_hardware: str
    base_price: float
    agreed_price: float
    discount_pct: float
    guardrail_status: str
    adk_validation: str
    paypal_order_id: str
    authorization_id: Optional[str] = None
    capture_id: Optional[str] = None
    webhook_status: str
    deal_lifecycle: str
    created_at: datetime
