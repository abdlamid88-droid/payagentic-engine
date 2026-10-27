from fastapi import APIRouter, HTTPException
from app.schemas.negotiation import NegotiationRequest, NegotiationResponse
from app.schemas.pricing_policy import AGENT_CATALOG
from app.engine.negotiator import EscrowNegotiationEngine
import re

router = APIRouter(prefix="/agent", tags=["Autonomous Sales Agent"])

@router.post("/negotiate", response_model=NegotiationResponse)
async def negotiate_deal(req: NegotiationRequest):
    policy = AGENT_CATALOG.get(req.package_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Invalid package ID.")

    # استخراج أي عرض سعري اقترحه المستخدم في نصه
    price_match = re.search(r"\$?(\d+(\.\d+)?)", req.message)
    proposed_price = float(price_match.group(1)) if price_match else policy.base_price_usd

    evaluation = EscrowNegotiationEngine.evaluate_offer(req.package_id, proposed_price)

    if evaluation["allowed"]:
        reply = (
            f"Offer of ${evaluation['settled_price']:.2f} accepted for {policy.package_id}. "
            f"Our deterministic escrow policy verified the margin. "
            f"Funds will be locked conditionally in PayPal escrow pending ADK integrity dry-run."
        )
        checkout_ready = True
        mock_order_id = f"ORD-PP-{abs(hash(req.session_id)) % 1000000}"
        approval_url = f"https://www.sandbox.paypal.com/checkoutnow?token={mock_order_id}"
    else:
        reply = (
            f"Cannot accept ${proposed_price:.2f}. "
            f"Policy floor for {policy.package_id} is strictly ${policy.floor_price_usd:.2f} "
            f"(Max discount: {int(policy.max_discount_pct * 100)}%). I can close at ${policy.floor_price_usd:.2f} right now."
        )
        checkout_ready = False
        approval_url = None
        mock_order_id = None

    return NegotiationResponse(
        session_id=req.session_id,
        reply=reply,
        current_offered_price=evaluation["settled_price"],
        guardrail_status=evaluation["verdict"],
        paypal_checkout_ready=checkout_ready,
        approval_url=approval_url,
        order_id=mock_order_id
    )
