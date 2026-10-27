from app.schemas.pricing_policy import AGENT_CATALOG
import re

class EscrowNegotiationEngine:
    @staticmethod
    def evaluate_offer(package_id: str, proposed_price: float) -> dict:
        policy = AGENT_CATALOG.get(package_id)
        if not policy:
            return {
                "verdict": "REJECT",
                "reason": "Package not found in registry.",
                "settled_price": 0.0
            }
        
        # الفحص الحتمي الصارم لسياسة السعر الأدنى لمنع الـ Prompt Injection
        if proposed_price < policy.floor_price_usd:
            return {
                "verdict": "GUARDRAIL_VIOLATION",
                "reason": f"Offered price ${proposed_price:.2f} is below strict floor ${policy.floor_price_usd:.2f}.",
                "settled_price": policy.floor_price_usd,
                "allowed": False
            }
        
        return {
            "verdict": "VERIFIED_PASS",
            "reason": "Offer satisfies margin and risk policy.",
            "settled_price": proposed_price,
            "allowed": True
        }
