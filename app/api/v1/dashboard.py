from fastapi import APIRouter
from typing import List
from app.schemas.dashboard import DealAuditRecord
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

AUDIT_LOG_STORE: List[DealAuditRecord] = [
    DealAuditRecord(
        transaction_id="TX-9402",
        package_id="coder-lora-gemma2-9b-swe",
        target_hardware="RTX_3060_12GB",
        base_price=120.0,
        agreed_price=96.0,
        discount_pct=20.0,
        guardrail_status="VERIFIED_PASS",
        adk_validation="PASS",
        paypal_order_id="8KJ19203AA90124",
        authorization_id="AUTH-492102-SANDBOX",
        capture_id="CAP-882109-SANDBOX",
        webhook_status="SIGNATURE_VERIFIED",
        deal_lifecycle="CAPTURED",
        created_at=datetime.utcnow()
    ),
    DealAuditRecord(
        transaction_id="TX-9403",
        package_id="enterprise-offline-audit-bundle",
        target_hardware="Local_Workstation_64GB",
        base_price=600.0,
        agreed_price=350.0,
        discount_pct=41.6,
        guardrail_status="OVERRIDE_REJECTED",
        adk_validation="PASS",
        paypal_order_id="5PP00192KK3321",
        authorization_id=None,
        capture_id=None,
        webhook_status="PENDING",
        deal_lifecycle="VOIDED",
        created_at=datetime.utcnow()
    )
]

@router.get("/deals", response_model=List[DealAuditRecord])
async def get_dashboard_deals():
    return AUDIT_LOG_STORE
