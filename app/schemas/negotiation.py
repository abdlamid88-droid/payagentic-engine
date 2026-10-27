from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatMessage(BaseModel):
    role: str
    content: str

class NegotiationRequest(BaseModel):
    session_id: str
    message: str
    package_id: str = "coder-lora-gemma2-9b-swe"
    target_hardware: Optional[str] = "RTX_3060_12GB"
    history: List[ChatMessage] = []

class NegotiationResponse(BaseModel):
    session_id: str
    reply: str
    current_offered_price: float
    guardrail_status: str
    paypal_checkout_ready: bool
    approval_url: Optional[str] = None
    order_id: Optional[str] = None
